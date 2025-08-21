function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function show_window(href, name)
{
    var win = window.open(href, id_to_windowname(name), 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
}

function close_window(win, id, name)
{
    document.getElementById(windowname_to_id(win.name)).value = id;
    document.getElementById(windowname_to_id(win.name) + '-label').innerHTML = name;
    win.close();
}
