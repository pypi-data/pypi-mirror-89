import os

from kabaret import flow
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict

from libreflow import baseflow
from .kitsu import KitsuEpisode
from .departments import Department


class ShotDepartments(flow.Object):
    layout = flow.Child(Department).ui(expanded=False)
    animation = flow.Child(Department).ui(expanded=True)
    compositing = flow.Child(Department).ui(expanded=True)


class Shot(baseflow.film.Shot):

    _episode = flow.Parent(4)
    departments = flow.Child(ShotDepartments).ui(expanded=True)

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set("%s/%s" % (
                self._episode.kitsu_url.get(),
                self.kitsu_id.get()
            ))


class Shots(baseflow.film.Shots):

    create_shot = flow.Child(baseflow.maputils.SimpleCreateAction)
    clear_shots = flow.Child(baseflow.maputils.ClearMapAction).ui(hidden=True)
    with flow.group('Kitsu'):
        toggle_kitsu_settings = flow.Child(baseflow.film.DisplayKitsuSettings)
        update_kitsu_settings = flow.Child(baseflow.film.UpdateItemsKitsuSettings)

    @classmethod
    def mapped_type(cls):
        return Shot


class Sequence(baseflow.film.Sequence):

    _episode = flow.Parent(2)
    shots = flow.Child(Shots).ui(default_height=420, expanded=True)
    compositing = flow.Child(Department).ui(expanded=True)

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set("%s/shots?search=%s" % (
                self._episode.kitsu_url.get(),
                self.name()
            ))


class Sequences(baseflow.film.Sequences):

    ICON = ('icons.flow', 'sequence')

    _episode = flow.Parent()

    create_sequence = flow.Child(baseflow.maputils.SimpleCreateAction)
    clear_sequences = flow.Child(baseflow.film.ClearSequencesAction).ui(hidden=True)
    update_kitsu_settings = flow.Child(baseflow.film.UpdateItemsKitsuSettings)

    @classmethod
    def mapped_type(cls):
        return Sequence
    
    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return self._episode.get_default_contextual_edits(context_name)


class Episode(KitsuEpisode):

    ICON = ('icons.flow', 'film')

    settings = flow.Child(ContextualView).ui(hidden=True)
    sequences = flow.Child(Sequences).ui(default_height=420, expanded=True)
    compositing = flow.Child(Department).ui(expanded=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(
                path=self.name(),
                episode=self.name()
            )


class Episodes(flow.Map):

    ICON = ('icons.flow', 'film')

    create_episode = flow.Child(baseflow.maputils.SimpleCreateAction)
    clear_episodes = flow.Child(baseflow.maputils.ClearMapAction)

    @classmethod
    def mapped_type(cls):
        return Episode
