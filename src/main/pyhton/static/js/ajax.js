function execute(myurl, successFunction) {
    var globalData;
    var result = $.ajax({url: myurl}
    ).done(function (data) {
            console.log("data:", data);
            successFunction(data);
            return data;
        });
}
function deletePocketItem(item) {
    var myurl = "pocket/delete?item=" + item;
    execute(myurl);
}

function archivePocketItem(item) {
    var myurl = "pocket/archive?item=" + item;
    execute(myurl);
}
