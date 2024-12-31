import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import argparse


def plot_task_schedule(task_data, title, annotations=None):
    """
    Plots a Gantt-like task schedule with optional annotations.

    Parameters:
    - task_data (dict): Dictionary containing task names and their active status.
    - title (str): Title of the plot.
    - annotations (list): List of dictionaries specifying annotations.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # Y-axis task labels
    task_names = list(task_data.keys())
    display_names = [task_info["name"] for task_info in task_data.values()]
    num_tasks = len(display_names)
    ax.set_yticks(range(num_tasks))
    ax.set_yticklabels(display_names)

    # Time axis (assuming uniform time steps)
    max_time = max(len(task["active"]) for task in task_data.values())
    ax.set_xticks(range(max_time))
    ax.set_xticklabels(range(1, max_time + 1))  # Time steps start from 1

    # Plot each task as horizontal blocks where active == 1
    box_height = 0.4  # Reduced height for rectangles
    for i, (task_name, task_info) in enumerate(task_data.items()):
        active_states = task_info["active"]
        for time_idx, active in enumerate(active_states):
            if active == 1:
                rect = patches.Rectangle(
                    (time_idx, i - box_height / 2),  # Center the rectangle vertically
                    1,  # Width of the rectangle
                    box_height,  # Height of the rectangle
                    facecolor=None,
                    edgecolor="hotpink",
                    lw=1.5,
                    hatch="////",
                )
                ax.add_patch(rect)

    # Add annotations if provided
    if annotations:
        for annotation in annotations:
            add_annotation(ax, annotation, task_names, box_height)

    # Beautify the plot
    ax.set_xlim(0, max_time)
    ax.set_ylim(-0.5, num_tasks - 0.5)
    ax.invert_yaxis()  # Invert Y-axis to align with input order
    ax.set_xlabel("Time")
    ax.set_ylabel("Tasks")
    ax.set_title(title)
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    # Add a legend for the hatched rectangle
    legend_patch = patches.Patch(
        facecolor="none", edgecolor="hotpink", hatch="////", label="Task Running"
    )
    ax.legend(handles=[legend_patch], loc="upper right", fontsize=10, frameon=True)

    plt.tight_layout()


def add_annotation(ax, annotation, task_names, box_height):
    """
    Adds an annotation to the plot based on task and time position.

    Parameters:
    - ax: Matplotlib Axes object to add annotation to.
    - annotation (dict): Annotation schema.
    - task_names (list): List of task identifiers to find task index.
    - box_height (float): Height of the rectangle to adjust text alignment.
    """
    task_index = task_names.index(annotation["task"])
    time_index = annotation["time"]
    position = annotation["position"]
    text = annotation["text"]

    # Adjust alignment based on position (start or end)
    if position == "start":
        ha_align = "left"
        x_pos = time_index + 0.05
    else:  # 'end'
        ha_align = "right"
        x_pos = time_index + 0.95

    y_pos = task_index

    ax.text(
        x_pos,
        y_pos,
        text,
        ha=ha_align,
        va="center",
        color="black",
        fontsize=8,
        fontweight="normal",
        bbox=dict(facecolor="white", edgecolor="none", boxstyle="round,pad=0.3"),
    )


def main():
    """Main function to parse arguments and plot the task schedule."""
    parser = argparse.ArgumentParser(description="Generate an RTOS task diagram.")
    parser.add_argument(
        "input_data_path",
        type=str,
        help="Path to JSON file containing task data.",
    )
    parser.add_argument("--output_path", type=str, help="Path to save the plot.")

    args = parser.parse_args()

    # Load task data from JSON file
    with open(args.input_data_path, "r") as file:
        input_data = json.load(file)

    # Run the function
    plot_task_schedule(
        input_data["task_data"], input_data["title"], input_data.get("annotations")
    )

    # Save or display the plot
    if args.output_path:
        plt.savefig(args.output_path)
    else:
        plt.show()


if __name__ == "__main__":
    main()
