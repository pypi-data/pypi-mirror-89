# Run any blocking command with systray icon

This is mainly useful for background processes.
It gives you an indication that it's running and allows
you to send a `SIGINT` signal by clicking on the `Quit` menu item.

```
# Install withtray
pip install --user withtray

# Copy your icon to ~/.local/share/icons and run
withtray 'polly server' --name polly --icon polly
```
