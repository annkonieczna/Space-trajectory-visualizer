from pathlib import Path

from animation import (
    animate_two_moving_points,
    animate_two_moving_points_on_static_trajectory,
)
from bodies import build_body_ellipsoid
from config import (
    ANIM_END_UTC,
    ANIM_START_UTC,
    ANIM_STEP_IN_SECONDS,
    CASSINI_NAME,
    DEFAULT_END_UTC,
    DEFAULT_START_UTC,
    DEFAULT_STEP_IN_SECONDS,
    META_KERNEL,
    SATURN_NAME,
    TITAN_NAME,
)
from spice_loader import clear_kernels, load_kernels
from time_utilis import generate_et_range
from trajectory import build_trajectory_dataframe
from visualization import (
    ensure_output_dir,
    plot_trajectory_3d,
    plot_two_trajectories_3d,
)


def main() -> None:
    output_dir = Path("output/plots/figures")
    output_anim_dir = Path("output/animation")
    ensure_output_dir(output_dir)
    ensure_output_dir(output_anim_dir)
    load_kernels(META_KERNEL)
    try:
        ets = generate_et_range(
            DEFAULT_START_UTC, DEFAULT_END_UTC, DEFAULT_STEP_IN_SECONDS
        )
        cassini_df = build_trajectory_dataframe(
            target=CASSINI_NAME, observer=SATURN_NAME, ets=ets
        )
        titan_df = build_trajectory_dataframe(
            target=TITAN_NAME, observer=SATURN_NAME, ets=ets
        )
        saturn_body = build_body_ellipsoid(
            body_name=SATURN_NAME, center_km=(0.0, 0.0, 0.0)
        )
        plot_trajectory_3d(
            df=cassini_df,
            title="Cassini trajectory around Saturn",
            output_path=output_dir / "Cassini_3d.html",
            central_body=saturn_body,
        )
        plot_two_trajectories_3d(
            df_a=cassini_df,
            df_b=titan_df,
            title_a="Cassini trajectory",
            title_b="Titan trajectory",
            title="Cassini and Titan trajectories relative to Saturn",
            output_path=output_dir / "Cassini-Titan3d.html",
            central_body=saturn_body,
        )
        # plot_trajectory_3d(
        #     df=cassini_df,
        #     title="Cassini",
        #     output_path=output_dir / "Cassini_3d.html",
        #     central_body=saturn_body,
        # )
        # plot_two_trajectories_3d(
        #     df_a=cassini_df,
        #     df_b=titan_df,
        #     title_a="Trajektoria Cassini",
        #     title_b="Trajektoria Tytana",
        #     title="Wspólna trajektoria Cassini i Tyttana względem Saturna",
        #     output_path=output_dir / "Cassini-Titan3d.html",
        #     central_body=saturn_body,
        # )
        ets_anim = generate_et_range(ANIM_START_UTC, ANIM_END_UTC, ANIM_STEP_IN_SECONDS)
        cassini_anim_df = build_trajectory_dataframe(
            target=CASSINI_NAME, observer=SATURN_NAME, ets=ets_anim
        )
        titan_anim_df = build_trajectory_dataframe(
            target=TITAN_NAME, observer=SATURN_NAME, ets=ets_anim
        )
        # animate_one_object_with_central_body_pyvista(
        #     df=cassini_anim_df,
        #     title="Cassini trajectory around Saturn",
        #     output_path=output_anim_dir / "cassini_pyvista.mp4",
        #     central_body=saturn_body,
        #     central_body_scale=1.0,
        #     frame_step=5,
        #     points_between=3,
        #     fps=30,
        #     duration_seconds=15,
        # )
        # animate_moving_point_on_static_trajectory(
        #     df=cassini_anim_df,
        #     title="Cassini trajectory around Saturn",
        #     output_path=output_anim_dir / "cassini_trajectory.html",
        #     central_body=saturn_body,
        #     central_body_scale=1.0,
        #     frame_step=2,
        #     points_between=3,
        #     animation_frames=700,
        #     frame_duration_ms=11,
        # )
        animate_two_moving_points_on_static_trajectory(
            df_a=cassini_anim_df,
            df_b=titan_anim_df,
            title="Cassini's and Titan's trajectory around Saturn",
            title_a="Cassini",
            title_b="Titan",
            output_path=output_anim_dir / "cassini_and_titan_trajectory.html",
            central_body=saturn_body,
            central_body_scale=1.0,
            frame_step=2,
            points_between=3,
            animation_frames=700,
            frame_duration_ms=11,
        )
        animate_two_moving_points(
            df_a=cassini_anim_df,
            df_b=titan_anim_df,
            title="Cassini's and Titan's trajectory around Saturn",
            title_a="Cassini",
            title_b="Titan",
            output_path=(
                output_anim_dir / "cassini_and_titan_trajectory_wo_the_lines.html"
            ),
            central_body=saturn_body,
            central_body_scale=1.0,
            frame_step=2,
            points_between=3,
            animation_frames=700,
            frame_duration_ms=11,
        )

        print(
            "Analysis complete. Figures saved to output/plots/figures "
            "and animation saved to output/animation"
        )
    finally:
        clear_kernels()


if __name__ == "__main__":
    main()
