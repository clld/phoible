<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" style="padding-top: 7px; padding-bottom: 5px;" href="${request.route_url('dataset')}"
       title="${request.dataset.name}">
        ##[ˈfɔɪ.bl̴]
        <img height="25" src="${request.static_url('phoible:static/phoible_icon.png')}"/>
    </a>
</%block>

${next.body()}

<script>
    // Add charissil CSS head to all views
    let charissil = "${request.static_url('clld:web/static/css/charissil.css')}";
    document.querySelector('head').innerHTML += '<link rel="stylesheet" href="' + charissil + '" type="text/css"/>';

    // Append Menu Items
    let menuUl = document.querySelector('#menuitem_sources').parentElement;
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

    // To correct fonts in tables
    async function corrections() {
        // Find all tables
        let table = document.querySelectorAll('table');
        if (table != null) {
            for (let i = 0; i < table.length; i++) {
                let tableId = table[i].id;
                let tableContent = table[i].getElementsByTagName('tbody')[0].children;
                // wait until table is loaded
                while (tableContent.length === 0) {
                    tableContent = table[i].getElementsByTagName('tbody')[0].children;
                    await new Promise(r => setTimeout(r, 100));
                }
                let ipaIndexes = [];
                try {
                    let colNames = table[i].getElementsByTagName('thead')[0].children[0].children;
                    let counter = 0;
                    // record indexes of the columns with "Name"(in Segments page), "Segment", and "Allophones"
                    Array.from(colNames).forEach(item => {
                        let colName = item.textContent.toLowerCase();
                        if ((colName === "name" && tableId === "Segments") || colName === "segment" || colName === "allophones") {
                            ipaIndexes.push(counter);
                        }
                        counter++;
                    });
                    // Add charissil class to the field
                    Array.from(ipaIndexes).forEach(index => {
                        Array.from(tableContent).forEach(item => {
                            let itemToBeChanged = item.children[index];
                            // If field has a child, usually it is a <a>
                            if (itemToBeChanged.children.length > 0) {
                                itemToBeChanged = item.children[index].children[0];
                            }
                            itemToBeChanged.classList.add('charissil');
                            // For testing, highlight display
                            // itemToBeChanged.style.color = 'red';
                        });
                    });
                } catch (e) {
                    // The table is not a full table
                }
            }
        }
    }

    // To correct fonts in tables
    async function ipaCorrections() {
        // ever anchor in the table
        let tables = document.querySelectorAll('table');
        Array.from(tables).forEach(table => {
            Array.from(table.querySelectorAll('a')).forEach(item => {
                item.classList.add('charissil');
                //item.style.color = 'red';
            });
        });
        // every anchor in the #vowels
        let vowelsDiv = document.querySelector('#vowels');
        Array.from(vowelsDiv.querySelectorAll('a')).forEach(item => {
            item.classList.add('charissil');
            //item.style.color = 'red';
        });
    }

    $(document).ready(function () {
        corrections();
        let counter = 0;
        // listener when the table info text is changed
        $('.dataTables_info').bind('DOMSubtreeModified', function () {
            if (counter++ >= 3) {
                corrections();
                counter = 0;
            }
        });

        // check if has links to IPA chart
        let anchors = document.querySelectorAll('a');
        for (let i = 0; i < anchors.length; i++) {
            if (anchors[i].href.endsWith("#ipa")) {
                anchors[i].id = "anchorId";
                anchors[i].parentElement.parentElement.id = "IPAAnchor";

                ipaCorrections();
                // listener for IPA charts
                let ipaCounter = 0;
                $('#IPAAnchor').bind('DOMSubtreeModified', function () {
                    if (ipaCounter++ >= 3) {
                        ipaCorrections();
                        ipaCounter = 0;
                    }
                });
            }
        }


    });
</script>