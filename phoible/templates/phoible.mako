<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" style="padding-top: 7px; padding-bottom: 5px;" href="${request.route_url('dataset')}" title="${request.dataset.name}">
        ##[ˈfɔɪ.bl̴]
        <img height="25" src="${request.static_url('phoible:static/phoible_icon.png')}"/>
    </a>
</%block>

${next.body()}

<script>
    let menuUl =  document.querySelector('#menuitem_sources').parentElement;
    let home_li = document.querySelector('#menuitem_dataset');
    let navbar_div = document.querySelector('#contextnavbar');

    let li1 = document.createElement('li');
    let li2 = document.createElement('li');
    li1.innerHTML = '<a href="/conventions" title="Conventions">Conventions</a>';
    li2.innerHTML = '<a href="/faq" title="FAQ">FAQ</a>';
    % if hasattr(context.get('request'), 'conventions'):
        li1.classList.add('active');
        home_li.classList.remove('active');
        navbar_div.remove();
    % endif
    % if hasattr(context.get('request'), 'faq'):
        li2.classList.add('active');
        home_li.classList.remove('active');
        navbar_div.remove();
    % endif
    menuUl.append(li1);
    menuUl.append(li2);
</script>