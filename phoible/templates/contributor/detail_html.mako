<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
    <%util:well>
        ${u.desc(request, ctx.description)|n}
    </%util:well>
</%def>

<h2>Contributor ${ctx.id}: ${ctx.name}</h2>

<%util:table args="item" items="${[a.contribution for a in ctx.contribution_assocs]}">
    <%def name="head()">
        <th>Language</th>
        <th>Source name</th>
        <th>Segments</th>
        ##<th></th>
    </%def>
    <td>${h.link(request, item)}</td>
    <td>${item.description}</td>
    <td>${item.count}</td>
</%util:table>