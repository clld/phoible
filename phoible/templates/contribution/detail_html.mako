<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<h2>${_('Contribution')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, contribution=ctx).render()}

<%def name="sidebar()">
    <%util:well title="Contributor">
        ${h.linked_contributors(request, ctx)}
        ${h.cite_button(request, ctx)}
    </%util:well>
    <%util:well>
        <h3>${h.link(request, ctx.language)}</h3>
        ${util.language_meta(lang=ctx.language)}
    </%util:well>
    <%util:well title="Sources">
        ${util.stacked_links(ref.source for ref in ctx.references)}
    </%util:well>
</%def>
