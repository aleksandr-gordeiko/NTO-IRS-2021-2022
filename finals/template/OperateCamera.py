import pyrealsense2 as rs
from enum import IntEnum
import open3d as o3d
import numpy as np


class OperateCamera:
    class Preset(IntEnum):
        Custom = 0
        Default = 1
        Hand = 2
        HighAccuracy = 3
        HighDensity = 4
        MediumDensity = 5

    def __init__(self, clipping_distance=2):
        # Configure depth and color streams
        # Create a pipeline
        self.pipeline = rs.pipeline()

        # Create a config and configure the pipeline to stream
        #  different resolutions of color and depth streams
        self.config = rs.config()

        # config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        # config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)

        # Start streaming
        profile = self.pipeline.start(self.config)
        self.depth_sensor = profile.get_device().first_depth_sensor()

        # Using preset HighAccuracy for recording
        self.depth_sensor.set_option(rs.option.visual_preset, self.Preset.HighAccuracy)

        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        self.depth_scale = self.depth_sensor.get_depth_scale()

        # We will not display the background of objects more than
        #  clipping_distance_in_meters meters away
        self.clipping_distance_in_meters = clipping_distance  # 3 meter

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def catch_frame(self):
        print('Started catching realsence data')
        for i in range(5):
            # Get frameset of color and depth
            frames = self.pipeline.wait_for_frames()

            # Align the depth frame to color frame
            aligned_frames = self.align.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            intrinsic = o3d.camera.PinholeCameraIntrinsic(
                self.__get_intrinsic_matrix(color_frame))

            # if aligned_depth_frame and color_frame:
            #     break

        depth_image = o3d.geometry.Image(
            np.array(aligned_depth_frame.get_data()))
        color_temp = np.asarray(color_frame.get_data())
        color_image = o3d.geometry.Image(color_temp)

        rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
            color_image,
            depth_image,
            depth_scale=1.0 / self.depth_scale,
            depth_trunc=self.clipping_distance_in_meters,
            convert_rgb_to_intensity=False)
        temp = o3d.geometry.PointCloud.create_from_rgbd_image(
            rgbd_image, intrinsic)
        flip_transform = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
        temp.transform(flip_transform)

        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = temp.points
        self.pcd.colors = temp.colors

        # o3d.io.write_point_cloud(f'{add_path}dataset/out.ply', pcd)
        print('Stopped catching realsence data')
        return self.pcd

    def save(self, filename):
        o3d.io.write_point_cloud(filename, self.pcd)

    def __get_intrinsic_matrix(self, frame):
        intrinsics = frame.profile.as_video_stream_profile().intrinsics
        out = o3d.camera.PinholeCameraIntrinsic(640, 480, intrinsics.fx,
                                                intrinsics.fy, intrinsics.ppx,
                                                intrinsics.ppy)
        return out

    @staticmethod
    def open(filename):
        return o3d.io.read_point_cloud(filename)

    @staticmethod
    def visualization_of_points(points):
        o3d.visualization.draw_geometries([points], 'Demonstration', 1080, 720)

    def stop(self):
        self.pipeline.stop()
