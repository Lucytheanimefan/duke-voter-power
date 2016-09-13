function scrapeSite() {
    var url = "http://projects.fivethirtyeight.com/2016-election-forecast/"
    $.get(url, function(data) {
        parseHTMLdata(data);
    });
}

scrapeSite();

function parseHTMLdata(htmlData) {
    console.log($.parseHTML(htmlData));
}

function mapDOM(element, json) {
    var treeObject = {};

    // If string convert to document Node
    if (typeof element === "string") {
        if (window.DOMParser) {
            parser = new DOMParser();
            docNode = parser.parseFromString(element, "text/xml");
        } else { // Microsoft strikes again
            docNode = new ActiveXObject("Microsoft.XMLDOM");
            docNode.async = false;
            docNode.loadXML(element);
        }
        element = docNode.firstChild;
    }

    //Recursively loop through DOM elements and assign properties to object
    function treeHTML(element, object) {
        object["type"] = element.nodeName;
        var nodeList = element.childNodes;
        if (nodeList != null) {
            if (nodeList.length) {
                object["content"] = [];
                for (var i = 0; i < nodeList.length; i++) {
                    if (nodeList[i].nodeType == 3) {
                        object["content"].push(nodeList[i].nodeValue);
                    } else {
                        object["content"].push({});
                        treeHTML(nodeList[i], object["content"][object["content"].length - 1]);
                    }
                }
            }
        }
        if (element.attributes != null) {
            if (element.attributes.length) {
                object["attributes"] = {};
                for (var i = 0; i < element.attributes.length; i++) {
                    object["attributes"][element.attributes[i].nodeName] = element.attributes[i].nodeValue;
                }
            }
        }
    }
    treeHTML(element, treeObject);

    return (json) ? JSON.stringify(treeObject) : treeObject;
}


var election = new Datamap({
    scope: 'usa',
    element: document.getElementById('map_election'),
    geographyConfig: {
        highlightBorderColor: '#bada55',
        popupTemplate: function(geography, data) {
            return '<div class="hoverinfo">' + geography.properties.name +
                '<br> Tipping Power: ' + data.tippingPower +
                '<br> Voting Power Index: ' + data.votingPowerIndex
        },
        highlightBorderWidth: 3
    },

    fills: {
        'Republican': '#CC4731',
        'Democrat': '#306596',
        'Heavy Democrat': '#667FAF',
        'Light Democrat': '#A9C0DE',
        'Heavy Republican': '#CA5E5B',
        'Light Republican': '#EAA9A8',
        defaultFill: '#EDDC4E'
    },
    data: { 'WA': { 'tippingPower': '0.7%', 'votingPowerIndex': '0.3' }, 'DE': { 'tippingPower': '0.3%', 'votingPowerIndex': '0.9' }, 'WI': { 'tippingPower': '6.8%', 'votingPowerIndex': '2.9' }, 'WV': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'HI': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.2' }, 'FL': { 'tippingPower': '15.5%', 'votingPowerIndex': '2.2' }, 'WY': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'NH': { 'tippingPower': '2.5%', 'votingPowerIndex': '4.6' }, 'NJ': { 'tippingPower': '3.3%', 'votingPowerIndex': '1.2' }, 'NM': { 'tippingPower': '1.8%', 'votingPowerIndex': '3.1' }, 'TX': { 'tippingPower': '0.7%', 'votingPowerIndex': '0.1' }, 'LA': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'NC': { 'tippingPower': '7.6%', 'votingPowerIndex': '2.2' }, 'ND': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.3' }, 'NE': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'TN': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'NY': { 'tippingPower': '0.2%', 'votingPowerIndex': '0.1' }, 'PA': { 'tippingPower': '10.6%', 'votingPowerIndex': '2.5' }, 'RI': { 'tippingPower': '0.9%', 'votingPowerIndex': '2.7' }, 'NV': { 'tippingPower': '3.7%', 'votingPowerIndex': '4.6' }, 'VA': { 'tippingPower': '5.1%', 'votingPowerIndex': '1.7' }, 'CO': { 'tippingPower': '5.5%', 'votingPowerIndex': '2.7' }, 'AK': { 'tippingPower': '0.3%', 'votingPowerIndex': '1.3' }, 'AL': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'AR': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'VT': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.6' }, 'IL': { 'tippingPower': '0.9%', 'votingPowerIndex': '0.2' }, 'GA': { 'tippingPower': '1.9%', 'votingPowerIndex': '0.6' }, 'IN': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'IA': { 'tippingPower': '2.3%', 'votingPowerIndex': '1.9' }, 'OK': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'AZ': { 'tippingPower': '1.9%', 'votingPowerIndex': '1.0' }, 'CA': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'ID': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'CT': { 'tippingPower': '0.6%', 'votingPowerIndex': '0.5' }, 'ME': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.4' }, 'MD': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'MA': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'OH': { 'tippingPower': '12.0%', 'votingPowerIndex': '2.9' }, 'UT': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'MO': { 'tippingPower': '0.3%', 'votingPowerIndex': '0.1' }, 'MN': { 'tippingPower': '3.4%', 'votingPowerIndex': '1.5' }, 'MI': { 'tippingPower': '8.0%', 'votingPowerIndex': '2.2' }, 'KS': { 'tippingPower': '0.2%', 'votingPowerIndex': '0.3' }, 'MT': { 'tippingPower': '0.2%', 'votingPowerIndex': '0.5' }, 'MS': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'SC': { 'tippingPower': '0.5%', 'votingPowerIndex': '0.3' }, 'KY': { 'tippingPower': '0.1%', 'votingPowerIndex': '0.1' }, 'OR': { 'tippingPower': '0.6%', 'votingPowerIndex': '0.5' }, 'SD': { 'tippingPower': '0.2%', 'votingPowerIndex': '0.5' } }
});
election.labels();
