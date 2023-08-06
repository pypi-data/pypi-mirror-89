import re
import os
from pathlib import Path

from kabaret import flow
from kabaret.flow_contextual_dict import get_contextual_dict

from libreflow import baseflow


class Revision(baseflow.file.Revision):
    
    playblast_path = flow.Computed()

    def has_playblast(self):
        return os.path.exists(self.playblast_path.get())

    def compute_child_value(self, child_value):
        if child_value is self.playblast_path:
            child_value.set(os.path.join(
                self._file.get_playblast_folder(),
                "%s_%s-movie.mov" % (self._file.complete_name.get(), self.name())
            ))
        else:
            super(Revision, self).compute_child_value(child_value)


class Revisions(baseflow.file.Revisions):

    @classmethod
    def mapped_type(cls):
        return Revision

    def columns(self):
        return super(Revisions, self).columns() + ['Playblast']
    
    def _fill_row_cells(self, row, item):
        super(Revisions, self)._fill_row_cells(row, item)
        row['Playblast'] = ''
    
    def _fill_row_style(self, style, item, row):
        super(Revisions, self)._fill_row_style(style, item, row)
        if item.has_playblast():
            style['Playblast_icon'] = ('icons.gui', 'youtube-logo')


class CreateTrackedFileAction(baseflow.file.CreateTrackedFileAction):

    def run(self, button):
        if button == 'Cancel':
            return

        settings = get_contextual_dict(self, 'settings')

        name = self.file_name.get()
        prefix = ""

        if 'episode' in settings:
            prefix = "{episode}_{sequence}_{shot}_{department}_"
        elif 'asset_type' in settings:
            prefix = "{asset_type}_{asset_name}_{department}_"
            
        prefix = prefix.format(**settings)

        self.root().session().log_debug('Creating file %s.%s' % (name, self.file_format.get()))

        self._files.add_tracked_file(name, self.file_format.get(), prefix + name)
        self._files.touch()


class RenderBlenderPlayblastAction(baseflow.file.OpenWithBlenderAction):

    _files = flow.Parent(2)
    revision_name = flow.Param('', baseflow.file.RevisionsChoiceValue).watched()

    def _sequence_number_from_name(self, sequence_name):
        tmp = re.findall(r'\d+', sequence_name)
        numbers = list(map(int, tmp))
        return numbers[0]
    
    def get_buttons(self):
        self.revision_name.revert_to_default()
        return ['Render', 'Publish first', 'Cancel']
    
    def needs_dialog(self):
        return True
    
    def allow_context(self, context):
        return context and not self._file.is_empty()

    def child_value_changed(self, child_value):
        if child_value is self.revision_name:
            msg = "Choosing to render a revision's playblast\
            will override the existing one."

            # Check if revision playblast exists
            revision = self._file.get_revision(child_value.get())
            if revision.has_playblast():
                msg = "<font color=#D50000>%s</font>" % msg
            
            self.message.set("<h3>Render playblast</h3>" + msg)

    def extra_argv(self):
        file_settings = get_contextual_dict(self._file, 'settings', ['sequence', 'shot'])
        project_name = self.root().project().name()
        revision = self._file.get_revision(self.revision_name.get())
        python_expr = """import bpy
bpy.ops.lfs.playblast(do_render=True, filepath='%s', studio='%s', project='%s', sequence='s%04i', scene='%s')""" % (
                revision.playblast_path.get().replace('\\', '/'),
                'LFS',
                project_name,
                self._sequence_number_from_name(file_settings['sequence']),
                file_settings['shot'],
            )

        return [
            "-b", revision.get_path(),
            "--addons", "mark_sequence",
            "--python-expr", python_expr
        ]
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        # Render playblast in a preview folder (may be more generic in the future)
        if not self._files.has_mapped_name('preview'):
            self._files.add_folder('preview')
            self._files.touch()
        
        if button == 'Publish first':
            return self.get_result(next_action=self._file.publish_and_render_playblast.oid())
        
        super(RenderBlenderPlayblastAction, self).run(button)


class PublishAndRenderPlayblastAction(baseflow.file.PublishFileAction):

    def run(self, button):
        if button == 'Cancel':
            return self.get_result(next_action=self._file.render_playblast.oid())

        super(PublishAndRenderPlayblastAction, self).run(button)
        published_revision = self._file.get_head_revision()
        
        self._file.render_playblast.revision_name.set(published_revision.name())

        return self._file.render_playblast.run('Render')


class TrackedFile(baseflow.file.TrackedFile):

    with flow.group('Playblast'):
        render_playblast = flow.Child(RenderBlenderPlayblastAction)
        publish_and_render_playblast = flow.Child(PublishAndRenderPlayblastAction)

    with flow.group('Open with'):
        open_with_blender = flow.Child(baseflow.file.OpenWithBlenderAction).ui(label='Blender')
        open_with_krita = flow.Child(baseflow.file.OpenWithKritaAction).ui(label='Krita')
        open_with_vscodium = flow.Child(baseflow.file.OpenWithVSCodiumAction).ui(label='VSCodium')
        open_with_notepadpp = flow.Child(baseflow.file.OpenWithNotepadPPAction).ui(label='Notepad++')
    
    def has_playblast(self):
        for rev in self.get_revisions().mapped_items():
            if rev.has_playblast():
                return True
        
        return False
    
    def get_playblast_folder(self):
        settings = get_contextual_dict(self._department, 'settings', ['ROOT_DIR', 'path'])
        return os.path.join(settings['ROOT_DIR'], settings['path'], 'preview')


class FileSystemMap(baseflow.file.FileSystemMap):

    def add_tracked_file(self, name, extension, complete_name):
        key = "%s_%s" % (name, extension)
        file = self.add(key, object_type=TrackedFile)
        file.format.set(extension)
        file.complete_name.set(complete_name)

        if self.root().project().admin.enable_filesystem_operations.get():
            # Create file folder
            try:
                self.root().session().log_debug("Create file folder '{}'".format(file.get_path()))
                os.makedirs(file.get_path())
            except OSError:
                self.root().session().log_error("Creation of file folder '{}' failed.".format(file.get_path()))
                pass

            # Create current revision folder
            current_revision_folder = os.path.join(file.get_path(), 'current')

            try:
                self.root().session().log_debug("Create current revision folder '{}'".format(current_revision_folder))
                os.mkdir(current_revision_folder)
            except OSError:
                self.root().session().log_error("Creation of current revision folder '{}' failed".format(current_revision_folder))
                pass

        return file

    def columns(self):
        return super(FileSystemMap, self).columns() + ['Playblast']
    
    def _fill_row_cells(self, row, item):
        super(FileSystemMap, self)._fill_row_cells(row, item)
        row['Playblast'] = ''
    
    def _fill_row_style(self, style, item, row):
        super(FileSystemMap, self)._fill_row_style(style, item, row)
        
        if hasattr(item, 'has_playblast') and item.has_playblast():
            style['Playblast_icon'] = ('icons.gui', 'youtube-logo')
