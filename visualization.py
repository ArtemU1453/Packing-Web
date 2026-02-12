def set_dark_axes_style(ax):
    ax.set_facecolor("#171A1E")
    ax.figure.set_facecolor("#0F1114")
    ax.tick_params(colors="#C9CDD1")
    ax.xaxis.label.set_color("#D8DCE0")
    ax.yaxis.label.set_color("#D8DCE0")
    ax.zaxis.label.set_color("#D8DCE0")

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((0.11, 0.13, 0.16, 0.35))
        axis.pane.set_edgecolor((0.40, 0.44, 0.49, 0.65))


def _roll_positions(box, roll, quantity):
    diameter = roll.diameter_mm
    roll_height = roll.width_mm

    if diameter <= 0 or roll_height <= 0:
        return []

    cols = int(box.width // diameter)
    rows = int(box.length // diameter)
    layers = int(box.height // roll_height)

    positions = []
    count = 0

    for z in range(layers):
        for x in range(cols):
            for y in range(rows):
                if count >= quantity:
                    return positions
                positions.append((x * diameter, y * diameter, z * roll_height, z))
                count += 1

    return positions


def build_layer_animation_data(box, roll, quantity):
    positions = _roll_positions(box, roll, quantity)
    if not positions:
        return [], 0

    max_layer = max(layer for _, _, _, layer in positions)
    return positions, max_layer


def draw_layered_frame(ax, box, roll, positions, current_layer, max_layer):
    ax.clear()
    set_dark_axes_style(ax)

    ax.bar3d(
        0,
        0,
        0,
        box.width,
        box.length,
        box.height,
        color="#9AA0A6",
        alpha=0.08,
        shade=False,
        edgecolor="#8A9097",
        linewidth=0.4,
    )

    visible = [p for p in positions if p[3] <= current_layer]
    for x, y, z, _ in visible:
        ax.bar3d(
            x,
            y,
            z,
            roll.diameter_mm,
            roll.diameter_mm,
            roll.width_mm,
            color="#B8C0C7",
            edgecolor="#6E7781",
            linewidth=0.25,
            alpha=0.92,
            shade=True,
        )

    ax.set_xlim(0, box.width)
    ax.set_ylim(0, box.length)
    ax.set_zlim(0, box.height)

    ax.set_xlabel("Ширина, мм")
    ax.set_ylabel("Длина, мм")
    ax.set_zlabel("Высота, мм")
    ax.set_title(
        f"Анимация укладки по слоям: слой {current_layer + 1} из {max_layer + 1}",
        color="#E3E7EB",
        pad=14,
    )
    ax.view_init(elev=24, azim=34)
