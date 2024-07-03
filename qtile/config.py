from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal ,send_notification
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration


import os
import subprocess
# Autostart
from libqtile import hook

@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([script])

@hook.subscribe.suspend
def lock_on_sleep():
    # Run screen locker
    qtile.spawn("/usr/bin/i3lock-fancy")

mod = "mod4"
alt = "mod3"
terminal = "kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([alt], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    
    # Same Above functions with arrow key
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),


    ### Layouts
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod],"f", lazy.window.toggle_fullscreen(),desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"],"Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack" ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod,"shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    
    ### APPS
    Key([mod], "b", lazy.spawn("firefox"), desc="WEB BROWSER"),
    Key([mod], "c", lazy.spawn("code"), desc="VISUAL STUDIO CODE / IDE"),
    Key([mod,"shift"], "f", lazy.spawn("pcmanfm"), desc="FILE BROWSER"),
    Key([mod], "p", lazy.spawn("keepassxc"), desc="KEEPASSXC / Password Manager"),
    Key([mod], "s", lazy.spawn("/home/punter/Applications/Spotube/spotube"), desc="Spotube/Music Client"),

    ### ROFI 
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Rofi drun"),
    Key([mod], "z", lazy.spawn("rofi -show combi"), desc="Rofi combi"),
    Key([mod,"shift"], "b", lazy.spawn("rofi -show filebrowser"), desc="Rofi Filebrowser"),
    
    ### Volume
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle"),desc="Mute/Unmute Volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%"),desc="Decrease Volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%"),desc="Increase Volume"),
    
    ### Media Keys
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"), 
   
    ### Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%"),desc="Increase Brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5-%"),desc="Decrease Brightness"),   

    ### FLAMESHOT
    Key([],"Print", lazy.spawn("flameshot full"),desc="Full Screenshot"),
    Key([mod,"shift"],"s", lazy.spawn("flameshot gui"),desc="Partial Screenshot"),

    ### LOCK SCREEN
    Key([mod], "x", lazy.spawn("i3lock-fancy"), desc="LockScreen"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7","8"]

#group_labels = ["1", "2", "3", "4", "5", "6", "7",]
group_labels = ["WEB", "TERM", "WORK", "MEDIA", "NOTE","CHAT", "GAME", "+", ]


group_layouts = ["monadtall", "monadtall", "tile", "tile", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))
 
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )


layouts = [
    layout.Tile(ratio=0.5,border_focus="#0000ff",shift_windows=True),
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4,margin=10),
    layout.Max(),    
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(margin=10,border_focus="#0000ff",border_width=2),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Fira Code",
    fontsize=15,
    padding=3,
    background="#000000",
    foreground="#9580ff",
    markup=True,
)
extension_defaults = widget_defaults.copy()

decoration_group1 = {
    "decorations": [
        RectDecoration(colour="#8e5ebc", radius=10, filled=True, padding_y=4, group=True)
    ],
    "padding": 10,
}
decoration_group2 = {
    "decorations": [
        RectDecoration(colour="#ff5252", radius=10, filled=True, padding_y=4, group=True)
    ],
    "padding": 10,
}
decor = {
    "decorations": [
        RectDecoration(colour="#2e3440", radius=10, filled=True, padding_y=5)
    ],
    "padding": 10,
}
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(**decor),
                widget.Spacer( background="#000000",length=10,),                
                #widget.CurrentLayoutIcon(),
                widget.GroupBox(foreground="#8aff80" ,highlight_method='text', hide_unused=False,disable_drag = True,active="#8aff80",padding_y=2,padding_x=3),
                widget.Spacer( background="#000000",length=10,),                
                widget.WindowName(center_aligned = True,**decoration_group1,foreground="#000000"),
                widget.Spacer( background="#000000",length=10,),                
                #widget.WidgetBox(widgets=[widget.Pomodoro(background="#6272a4",length_pomodri="60"),widget.SDD()]),
                widget.OpenWeather(**decor,center_aligned=True,app_key="eda42cf47435958fc7e4c35b624b1eb7",coordinates={"longitude": "80.1575", "latitude": "13.0319"},city="Porur,IN",markup=True,url="https://openweathermap.org/city/1465622",threshold=50, foreground_alert='ff6000',location="Chennai",format='{location_city}: {icon}{main_temp} °{units_temperature} {humidity}% {weather_details}'),
                #widget.OpenWeather(app_key="eda42cf47435958fc7e4c35b624b1eb7",coordinates={"longitude": "76.644", "latitude": "9.7493"},city="Valavoor,IN",markup=True,url="https://openweathermap.org/city/1272022",threshold=50, foreground_alert='ff6000'),
                widget.Spacer( background="#000000",length=10,),                
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                #widget.StatusNotifier(),
                widget.Clock( format = "⏱ %a, %b %d - %H:%M",**decor),
                widget.Spacer( background="#000000",length=10,),
                widget.Systray(padding=3),
                widget.Spacer( background="#000000",length=10,),
                widget.QuickExit(foreground ="#000000",default_text=" EXIT ",**decoration_group2),
            ],
            30,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X10 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
         x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="KeePassXC"),
        Match(wm_class="keepassxc"),
        Match(wm_class="nitrogen"),
        Match(wm_class="motrix"),
        Match(wm_class="Conky"),
        Match(wm_class="eww"),
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class="notification"),   # notifications
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(title="pinentry"),          # GPG key password entry

    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

@hook.subscribe.client_new
def new_client(client):
    #1 
    if client.name == "firefox":
        client.togroup("1")
    elif client.name == "motrix":
        client.togroup("1")
    #2
    elif client.name == "kitty":
        client.togroup("2")
    elif client.name == "pcmanfm":
        client.togroup("2")
    elif client.name == "dolphin":
        client.togroup("2")
    elif client.name == "nitrogen":
        client.togroup("2")
    elif client.name == "Konsole":
        client.togroup("2")

    #3    
    elif client.name == "libreoffice":
        client.togroup("3")
    elif client.name == "onlyoffice":
        client.togroup("3")
    elif client.name == "gimp":
        client.togroup("3")
    elif client.name == "superproductivity":
        client.togroup("3")
    
    #4
    elif client.name == "vlc":
        client.togroup("4")
    elif client.name == "spotube":
        client.togroup("4")
    elif client.name == "mpv":
        client.togroup("4")
    elif client.name == "freetube":
        client.togroup("4")
    elif client.name == "GwenView":
        client.togroup("4")

    #5
    elif client.name == "code":
        client.togroup("5")
    elif client.name == "kwrite":
        client.togroup("5")
    elif client.name == "ghostwriter":
        client.togroup("5")
    elif client.name == "com.github.xournalpp.xournalpp":
        client.togroup("5")
    
    #6
    elif client.name == "thunderbird":
        client.togroup("6")
    elif client.name == "telegram":
        client.togroup("6")
        #elif client.name == "GwenView":
    #    client.togroup("4")

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG2D"
