# A simple list explorer ipywidget.

import ipywidgets as widgets
from IPython.display import display

# Make scroll bar look normal
SCROLL_BAR_STYLE = """<style>
.light-scrollbar::-webkit-scrollbar {
    width: 8px;
    height: 8px;
    background-color: #f1f1f1;
}

.light-scrollbar::-webkit-scrollbar-thumb {
    background-color: #c1c1c1;
    border-radius: 4px;
}

.light-scrollbar::-webkit-scrollbar-thumb:hover {
    background-color: #a0a0a0;
}

/* Standard scrollbar properties for Firefox */
.light-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #c1c1c1 #f1f1f1;
}
</style>
"""


def create_scrollable_text_display(text="") -> tuple[widgets.HTML, callable]:
    """Scrollable text display with proper text wrapping.

    Returns the widget & a updater function for it"""
    html_widget = widgets.HTML(
        value=text,
        layout=widgets.Layout(
            height="100%",
            width="100%",
            overflow="auto",  # Enable scrolling
            padding="10px",
            margin="0",
        ),
    )

    def update_text(new_text):
        # Replace newlines with <br> tags for proper HTML line breaks
        formatted_text = new_text.replace("\n", "<br>")

        # Update content with CSS for word wrapping
        html_widget.value = f"""
        <div style="
            width: 100%; 
            word-wrap: break-word; 
            word-break: break-word;
            white-space: normal; 
            font-family: arial;
            line-height: 1.5;
        ">{formatted_text}</div>
        """

    return html_widget, update_text


def show_list_explorer(items: list[str], height=400, is_height_max=False):
    """Shows items in two views -> list view and detail view.

    If is_height_max then the passed height acts as a max height. Else we preserve height

    Can use `\\n` to add spaces in detail. List view is mono-line"""
    current_idx = 0

    ### Detail view
    # Back, Index Text
    back_button = widgets.Button(
        description="<- Back to List",
        button_style="info",
        layout=widgets.Layout(
            width="20%",
            height="100%",
        ),
    )
    index_text = widgets.Label("")

    # Prev/Next buttons
    prev_button = widgets.Button(
        description="< Previous",
        button_style="info",
        layout=widgets.Layout(height="100%", width="50%"),
    )
    next_button = widgets.Button(
        description="Next >",
        button_style="info",
        layout=widgets.Layout(height="100%", width="50%"),
    )
    direction_button_container = widgets.HBox(
        [prev_button, next_button],
        layout=widgets.Layout(
            width="20%",
            height="100%",
            flex="0 0 auto",  # Prevent shrinking
        ),
    )

    subtitle_container = widgets.HBox(
        [back_button, index_text, direction_button_container],
        layout=widgets.Layout(
            width="100%",
            justify_content="space-between",
            flex="0 0 auto",  # Prevent shrinking
            padding="3px",
        ),
    )

    expanded_section, update_expand_section = create_scrollable_text_display("")
    expanded_section.add_class("light-scrollbar")
    detail_view = widgets.VBox(
        [subtitle_container, expanded_section],
        layout=widgets.Layout(
            width="100%",
        ),
    )

    ## List view
    item_buttons = []
    for i, item in enumerate(items):
        btn = widgets.Button(
            description=f"{i+1}.{item}",
            button_style="",
            layout=widgets.Layout(
                width="100%",
                height="30px",
                flex="0 0 auto",  # remove flex basis, makes them shrink
                margin="0",
                display="flex",
                justify_content="flex-start",
            ),
        )
        btn.index = i  # Store item index for reference
        item_buttons.append(btn)

    list_container = widgets.VBox(
        item_buttons,
        layout=widgets.Layout(
            grid_gap="4px", overflow="scroll", width="100%", height="100%"
        ),
    )
    list_container.add_class("light-scrollbar")

    main_view = widgets.Stack(
        [list_container, detail_view],
        selected_index=0,
        layout=widgets.Layout(
            width="100%",
            height=None if is_height_max else f"{height}px",
            max_height=f"{height}px" if is_height_max else None,
            padding="10px",
        ),
    )

    # Wrap once more to add custom css styles
    css_widget = widgets.HTML(SCROLL_BAR_STYLE)
    app = widgets.VBox([css_widget, main_view])

    ### Functionality & handlers
    def show_list_view():
        main_view.selected_index = 0

    def show_detail_view(idx):
        nonlocal current_idx
        current_idx = idx

        main_view.selected_index = 1

        # Update button states
        prev_button.disabled = current_idx == 0
        next_button.disabled = current_idx == len(items) - 1

        # Update index text
        index_text.value = f"Item {current_idx + 1} of {len(items)}"

        # Display details in expanded section
        update_expand_section(items[current_idx])

    # Button callback handlers
    def on_item_click(b):
        show_detail_view(b.index)

    def on_back_click(b):
        show_list_view()

    def on_prev_click(b):
        if current_idx > 0:
            show_detail_view(current_idx - 1)

    def on_next_click(b):
        if current_idx < len(items) - 1:
            show_detail_view(current_idx + 1)

    for btn in item_buttons:
        btn.on_click(on_item_click)
    back_button.on_click(on_back_click)
    prev_button.on_click(on_prev_click)
    next_button.on_click(on_next_click)

    display(app)