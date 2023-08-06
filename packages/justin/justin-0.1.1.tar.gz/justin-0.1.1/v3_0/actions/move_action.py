from argparse import Namespace
from typing import List

from pyvko.models.group import Group

from v3_0.actions.action import Action
from v3_0.actions.checks_runner import ChecksRunner
from v3_0.actions.named.stage.exceptions.check_failed_error import CheckFailedError
from v3_0.actions.named.stage.logic.base.check import Check
from v3_0.shared.filesystem.folder_tree import FolderTree
from v3_0.shared.helpers import util
from v3_0.shared.models.photoset import Photoset
from v3_0.shared.models.world import World


class MoveAction(Action):

    def __init__(self, prechecks: List[Check]) -> None:
        super().__init__()

        self.__prechecks = prechecks

    def perform(self, args: Namespace, world: World, group: Group) -> None:
        all_locations = world.all_locations

        paths = list(util.resolve_patterns(args.name))

        if not paths:
            return

        path = paths[0]

        path_location = world.location_of_path(path)

        new_locations = [loc for loc in all_locations if loc != path_location]

        if len(new_locations) == 0:
            print("Current location is the only available.")

            # number of locations is global, photoset may have only one location -> other's can't be moved too
            return
        elif len(new_locations) == 1:
            selected_location = new_locations[0]
        else:
            selected_location = util.ask_for_choice(f"Where would you like to move {path.name}?", new_locations)

        for path in paths:
            from_location = world.location_of_path(path)

            photoset = Photoset(FolderTree(path))

            try:
                ChecksRunner.instance().run(photoset, self.__prechecks)

                new_path = selected_location / photoset.path.parent.relative_to(from_location)

                photoset.move(new_path)

            except CheckFailedError as error:
                print(f"Unable to move {photoset.name}: {error}")
