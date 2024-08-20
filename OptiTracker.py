import datatable as dt
from typing import Tuple, Dict, List
from NatNetClient import NatNetClient


class OptiTracker:
    def __init__(self) -> None:
        # NatNetClient instance
        self.client = NatNetClient()

        self.active_listeners = {
            'Prefix': True,
            'MarkerSets': True,
            'LabeledMarkers': False,
            'LegacyMarkerSets': False,
            'RigidBodies': True,
            'Skeletons': False,
            'AssetRigidBodies': False,
            'AssetMarkers': False,
            'ForcePlates': False,
            'Devices': False,
            'Cameras': False,
            'Suffix': False,
        }

        self.asset_frames = {
            'Prefix': dt.Frame(),
            'MarkerSets': dt.Frame(),
            'LabeledMarkers': dt.Frame(),
            'LegacyMarkerSets': dt.Frame(),
            'RigidBodies': dt.Frame(),
            'Skeletons': dt.Frame(),
            'AssetRigidBodies': dt.Frame(),
            'AssetMarkers': dt.Frame(),
            'ForcePlates': dt.Frame(),
            'Devices': dt.Frame(),
            'Suffix': dt.Frame(),
        }

        self.asset_descriptions = {
            'MarkerSets': dt.Frame(),
            'LabeledMarkerSets': dt.Frame(),
            'LegacyMarkerSets': dt.Frame(),
            'RigidBodies': dt.Frame(),
            'Skeletons': dt.Frame(),
            'AssetRigidBodies': dt.Frame(),
            'AssetMarkers': dt.Frame(),
            'ForcePlates': dt.Frame(),
            'Devices': dt.Frame(),
            'Cameras': dt.Frame(),
        }

    # Create NatNetClient instance
    def init_client(self) -> object:
        client = NatNetClient()

        # Assign listener callbacks
        client.frame_data_listener = self.collect_frames
        client.description_listener = self.collect_descriptions

        return client

    # Plug into Motive stream
    def start_client(self) -> None:
        self.client.startup()

    # Stop NatNetClient
    def stop_client(self) -> None:
        self.client.shutdown()

    # streamdata collection callbacks

    def collect_frames(self, frame_data: Dict[str, List[Dict]]) -> None:
        for asset_type in frame_data.keys():
            for asset_data in frame_data[asset_type]:
                print(f'asset_data:\n{asset_data}')
                self.asset_frames[asset_type].rbind(dt.Frame(asset_data))

    def collect_descriptions(
        self, descriptions: Dict[str, Tuple[Dict, ...]]
    ) -> None:
        for asset_type, asset_description in descriptions.items():
            self.asset_descriptions[asset_type].rbind(
                dt.Frame(asset_description)
            )

    # Return frame and reset to None
    def export_frames(self) -> Dict[str, dt.Frame]:
        return self.asset_frames

    # Return frame and reset to None
    def descexport(self) -> Dict[str, dt.Frame]:
        return self.asset_descriptions
