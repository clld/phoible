<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>


<h2>${_('Language')} ${ctx.name}</h2>

<table class="table table-nonfluid table-condensed">
    <tbody>
    <tr>
        <td>WALS genus:</td>
        <td>${h.external_link('http://wals.info/languoid/genus/' + ctx.wals_genus_id, label=ctx.wals_genus) if ctx.wals_genus else ''}</td>
    </tr>
    <tr>
        <td>Number of speakers:</td>
        <td>${ctx.population or ctx.population_comment.replace('_', ' ')}</td>
    </tr>
    </tbody>
</table>

<h3>Inventories</h3>
<ul>
    % for inventory in ctx.inventories:
    <li>${h.link(request, inventory)}</li>
    % endfor
</ul>

<%def name="sidebar()">
    ${util.codes()}
    <div style="clear: right;"> </div>
    % if ctx.latitude is not None:
    <%util:well>
        ${request.map.render()}
        ${h.format_coordinates(ctx)}
    </%util:well>
    % endif
</%def>
