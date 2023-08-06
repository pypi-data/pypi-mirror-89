#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

from .video import Video
from .shapes import Circle


def bouncing_ball(path: str) -> None:
    """
    Bouncing ball animation.
    :param path: Path to export final video.
    """
    ball = Circle((50, 50), 50, (255, 255, 255, 255))
    ball.keyframe(0, "loc_x", 960)
    ball.keyframe(0, "loc_y", 50)
    ball.keyframe(30, "loc_y", 1030)
    ball.keyframe(55, "loc_y", 50)
    ball.keyframe(75, "loc_y", 1030)
    ball.keyframe(90, "loc_y", 50)
    ball.keyframe(100, "loc_y", 1030)
    ball.keyframe(105, "loc_y", 50)
    ball.keyframe(110, "loc_y", 1030)
    ball.keyframe(120, "loc_y", 50)
    ball.keyframe(135, "loc_y", 1030)
    ball.keyframe(155, "loc_y", 50)
    ball.keyframe(180, "loc_y", 1030)
    ball.keyframe(210+0, "loc_y", 50)
    ball.keyframe(210+30, "loc_y", 1030)
    ball.keyframe(210+55, "loc_y", 50)
    ball.keyframe(210+75, "loc_y", 1030)
    ball.keyframe(210+90, "loc_y", 50)
    ball.keyframe(210+100, "loc_y", 1030)
    ball.keyframe(210+105, "loc_y", 50)
    ball.keyframe(210+110, "loc_y", 1030)
    ball.keyframe(210+120, "loc_y", 50)
    ball.keyframe(210+135, "loc_y", 1030)
    ball.keyframe(210+155, "loc_y", 50)
    ball.keyframe(210+180, "loc_y", 1030)

    video = Video((1920, 1080), 30)
    video.add_layer(ball)
    video.export(path, 420)