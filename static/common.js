function validate() {
    var image = document.forms['myForm']['image'];
    var validExt = ["jpeg", "jpg"];

    if (document.myForm.firstname.value == "") {
        alert("Please provide your first name!");
        document.myForm.firstname.focus();
        return false;
    }
    if (document.myForm.lastname.value == "") {
        alert("Please provide your last name!");
        document.myForm.lastname.focus();
        return false;
    }
    if (document.myForm.phone.value == "") {
        alert("Please provide your Phone!");
        document.myForm.phone.focus();
        return false;
    }
    if (document.myForm.course.value == "") {
        alert("Please provide your course!");
        return false;
    }
    if (document.myForm.gender.value == "") {
        alert("Please provide your gender!");
        return false;
    }

    if (image.value != '') {
        var imageExt = image.value.substring(image.value.lastIndexOf('.') + 1);
        var result = validExt.includes(imageExt);

        if (result == false) {
            alert("Selected file is not an Image...");
            return false;
        } else {
            if (parseFloat(image.files[0].size / (1024 * 1024)) >= 3) {
                alert("File must be size less than 3 mb");
                return false;
            }
        }
    }
}


$('#countryId').on('change', function () {              // state dropdown
    $("#stateId").empty();
    $("#cityId").empty();
    var countryId = $(this).val();
    $.ajax({
        url: '/state',
        type: 'post',
        dataType: 'json',
        data: {
            countryData: countryId
        },
        success: function (stateResult) {
            let htmlData = '<option value="">State</option>'
            $.each(stateResult, function (stateId, stateName) {
                htmlData += '<option value="' + stateId + '">' + stateName + '</option>'

            });
            $('#stateId').html(htmlData)
        }
    })
});


// form ajax
$('#stateId').on('change', function () {          // city dropdown
    var stateId = $(this).val();
    $.ajax({
        url: '/city',
        type: 'post',
        dataType: 'json',
        data: {
            stateData: stateId
        },
        success: function (cityResult) {
            let htmlData = '<option value="">City</option>'
            $.each(cityResult, function (index, value) {
                htmlData += '<option value="' + index + '">' + value + '</option>'
            });
            $('#cityId').html(htmlData)
        }
    })
});


// update ajax
$(document).ready(function () {
    var countryId = $('#country').val();
    getState(countryId);
})

$('#country').on('change', function () {
    $("#state").empty(); $("#city").empty();
    var countryId = $(this).val();
    getState(countryId);
});

function getState(countryId) {
    $.ajax({
        url: '/state',
        type: 'post',
        dataType: 'json',
        data: {
            countryData: countryId
        },
        success: function (stateResult) {

            var element = $('[name="stateId"]').val();
            var stateId = parseInt(element);
            let htmlData = '<option value="">State</option>'
            $.each(stateResult, function (stateid, stateName) {
                if (stateid == stateId) {
                    htmlData += '<option value="' + stateid + '" selected> ' + stateName + '</option>'
                }
                else {
                    htmlData += '<option value="' + stateid + '">' + stateName + '</option>'
                }

            });
            $('#state').html(htmlData)
        }
    })
}

$(document).ready(function () {
    var stateId = $('[name="stateId"]').val();

    getCity(stateId);
})

$('#state').on('change', function () {
    var stateId = $(this).val();
    getCity(stateId);
});

function getCity(stateId) {
    $.ajax({
        url: '/city',
        type: 'post',
        dataType: 'json',
        data: {
            stateData: stateId
        },
        success: function (cityResult) {

            var element = $('[name="cityid"]').val();
            var cityid = parseInt(element);
            let htmlData = '<option value="">City</option>'
            $.each(cityResult, function (cityId, cityName) {
                if (cityId == cityid) {
                    htmlData += '<option value="' + cityId + '" selected> ' + cityName + '</option>'
                }
                else {
                    htmlData += '<option value="' + cityId + '">' + cityName + '</option>'
                }
            });
            $('#city').html(htmlData)
        }
    })
}

// display ajax
var pageSize = 5;
var pageLen = $('#page').val()
var pageCount = 0;
createButton(pageLen, 1)
function createButton(pageLen, currentPage) {
    pageCount = Math.ceil(pageLen / pageSize);
    $('#pagin').empty()
    let beforePage = currentPage;
    var difference = pageCount - currentPage;
    if (difference <= 3) {
        beforePage = pageCount - 3;
    }
    if (beforePage <= 0) {
        beforePage = 1;
    }
    if (pageCount < 3) {
        afterPage = beforePage + (pageCount - 1)
    } else {
        afterPage = beforePage + 3
    }
    if (afterPage > pageCount) {
        afterPage = pageCount
    }
    $('#pagin').append('<li class="firstPage"><a href="#"> << </a></li> ')
    $('#pagin').append('<li><a href="#" class="prev"> Prev </a></li>')

    for (var i = beforePage; i <= afterPage; i++) {
        if (i == currentPage) {
            $("#pagin").append('<li class="pageNumber current"><a href="#" id="' + i + '">' + i + '</a></li> ');
        } else {
            $("#pagin").append('<li class="pageNumber"><a href="#" id="' + i + '">' + i + '</a></li> ');
        }
    }
    if (currentPage == 1) {
        $('.prev').hide();
        $('.firstPage').hide();
    }

    $('#pagin').append('<li><a href="#" class="next"> Next </a></li> ')
    $('#pagin').append('<li class="lastPage"><a href="#"> >> </a></li> ')
    if (currentPage == 1) {
        $("#pagin li.pageNumber").first().addClass("current");
    }
    if (currentPage == pageCount) {
        $('.next').hide();
        $('.lastPage').hide();
    } else {
        $('.next').show();
        $('.lastPage').show();
    };
    showPage(1);
}

function showPage(page) {
    $("#page").hide();
    $("#page").each(function (n) {
        if (n >= pageSize * (page - 1) && n < pageSize * page)
            $(this).show();
    });
}

$('body').on('click', "#pagin li.pageNumber", function () {
    $("#pagin li").removeClass("current");
    $(this).addClass("current");
    showPage(parseInt($(this).find('a').text()))
    var pageId = $(this).find('a').text()
    ajaxFunction(pageId);

});

$('body').on('click', "#pagin li.firstPage", function () {
    $("#pagin li").removeClass("current");
    $('.pageNumber').find('a[id="1"]').closest('li').addClass('current');
    var pageId = 1;
    ajaxFunction(pageId);
});

$('body').on('click', "#pagin li.lastPage", function () {
    $("#pagin li").removeClass("current");
    $('.pageNumber').find('a[id="' + pageCount + '"]').closest('li').addClass('current');
    var pageId = pageCount;
    ajaxFunction(pageId);
});

$('body').on('click', ".next", function () {
    $('#pagin').find('.pageNumber.current').next().addClass('current');
    $('#pagin').find('.pageNumber.current').prev().removeClass('current');
    ajaxFunction($('#pagin').find('.pageNumber.current').text());
    console.log($('#pagin').find('.pageNumber.current').text());
});

$('body').on('click', ".prev", function () {
    ajaxFunction($('#pagin').find('.pageNumber.current').text() - 1);
});


function ajaxFunction(pageId) {
    if (pageId == 1) {
        $('.prev').hide();
        $('.firstPage').hide();
    } else {
        $('.prev').show();
        $('.firstPage').show();
    }

    if (pageId == pageCount) {
        $('.next').hide();
        $('.lastPage').hide();
    } else {
        $('.next').show();
        $('.lastPage').show();
    }

    var input = $('#myInput').val().toLowerCase();
    $.ajax({
        url: '/getRecords',
        type: 'post',
        dataType: 'json',
        data: {
            pageId: pageId,
            input: input
        },
        success: function (resultData) {
            htmlData = '';
            var pageLen = resultData['totalCount']
            createButton(pageLen, pageId)
            $('table#myTable > tbody').empty();
            $.each(resultData['data'], function (index, value) {
                console.log(value['id'])
                $('table#myTable > tbody').append('<tr><td>' + value['id'] + '</td><td>' + value['fname'] + '</td><td>' + value['lname'] + '</td><td>' + value['phone'] + '</td><td>' + value['course'] + '</td><td>' + value['gender'] + '</td><td>' + value['name'] + '</td><td>' + value['sname'] + '</td><td>' + value['cname'] + '</td><td>' + value['address'] + '</td><td>' + value['vehicle'] + '</td><td><img src="' + value['image'] + '" width="100px" height="100px"></td><td><a class="btn btn-warning" href="/update/' + value['id'] + '">Edit</a></td><td><a class="btn btn-warning" href="/delete/' + value['id'] + '">Delete</a></td></tr>');
            });
        }
    });
};

$("#myInput").on("keyup", function () {
    var input = $(this).val().toLowerCase();
    $('ul#pagein').empty()
    if (input != "") {
        $.ajax({
            url: "/search",
            type: "post",
            dataType: 'json',
            data: {
                input: input
            },
            success: function (data) {
                htmlData = '';
                pageLen = data['totalCount']
                $('ul#pagin').empty()
                createButton(pageLen, 1)
                $('table#myTable > tbody').empty();
                $.each(data['data'], function (index, value) {
                    $('table#myTable > tbody').append('<tr><td>' + value['id'] + '</td><td>' + value['fname'] + '</td><td>' + value['lname'] + '</td><td>' + value['phone'] + '</td><td>' + value['course'] + '</td><td>' + value['gender'] + '</td><td>' + value['name'] + '</td><td>' + value['sname'] + '</td><td>' + value['cname'] + '</td><td>' + value['address'] + '</td><td>' + value['vehicle'] + '</td><td><img src="' + value['image'] + '" width="100px" height="100px"></td><td><a class="btn btn-warning" href="/update/' + value['id'] + '">Edit</a></td><td><a class="btn btn-warning" href="/delete/' + value['id'] + '">Delete</a></td></tr>');
                });
            }
        });
    } else {
        var pageId = 1;
        ajaxFunction(pageId);
    }
});