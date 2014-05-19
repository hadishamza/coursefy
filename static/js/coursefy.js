$( document ).ready(function() {
    var localdata = JSON.parse(localStorage.getItem("synced_data"));

    var data = localdata || original_data;
    var course_data = [];


    /* Helper methods */
    function init_td(x, y, free) {
        free = (typeof free === "undefined") ? true : free;
        return {x: x, y: y, free: free};
    }

    function course_class(course_code) {
        var type_class;
        switch(course_code.substring(1,3)) {
            case "MS":
            case "MA":
                type_class = "math";
                break;
            case "FE":
                type_class = "fe";
                break;
            default:
                type_class = "tech";
                break;
        }

        return type_class;
    }

    /* Populate methods */
    var $studyplans = $(".studyplan");

    $studyplans.each(function(index, studyplan) {
        if (!localdata) {
            manage_data(data);
            init_studyplan_pos(data, index+1);

        }
        else {
            course_data = data;
        }

        init_grid($(studyplan), course_data, index+1)
        populate_studyplan($(studyplan), course_data, index+1);

    });
    function year_data(data, year){
        var data_year = [];
        data.forEach(function (course) {
            var course_year = parseInt(course["period"].substring(0,1));
            if (course_year === year) {
                data_year.push(course);
            }
        });
        return data_year;
    }

    function init_studyplan_pos(data, year) {
        var data_year = year_data(data, year);
        var num_rows = find_rows_num(data_year, year);
        var start_period = 1+(year*10);
        var i;
        for (i = 0; i < num_rows; i++) {
            var k = 0;
            for (var period = start_period; period <= (start_period+3); period++) {
                var dup;
                for(var j = 0; j < data_year.length; j++) {
                    dup = false;
                    var course = data_year[j];
                    var course_period = parseInt(course["period"]);
                    if (course_period === period) {
                        data_year.splice(j, 1);
                        if (!course.position)
                            course.position = {x: k, y: i};

                        if (course.dup){
                            period++;
                            k++;
                        }
                        course_data.push(course);
                        break;
                    }
                }
                k++;
            }
        }
    }


    function populate_studyplan($studyplan, data, year) {
        var data_year = year_data(data, year);
        var num_rows = find_greatest_y(data_year);
        $studyplan.find("tbody > tr").each(function(y) {
            var $tr = $(this);
            $tr.children("td").each(function(x) {
                var $td = $(this);
                var position = {x:$td.data("x"), y:$td.data("y")};
                var course = find_course_by_pos(data_year, position);
                if (course) {
                    $td.html("<div class='course'><div class='removeCourse'></div><div class='expandCourse'></div><div>" + course["code"] + "  " + course["level"] + " <strong>" + course["credits"] +"HP</strong> <br>" + course["name"] + " y:" + String(course.position.y) + " x:" + String(course.position.x) + "</div></div>");
                    var $course = $td.children(".course");
                    $course.data("course", course);
                    $course.addClass(course_class(course.code));
                    drop_help($td, course.dup, false);
                    if(course.dup) {
                        $course.find(".expandCourse").addClass("rotated");
                        $course.addClass("extend");
                    }
                }
            })
        });
    }

    function find_course_by_pos(data, position) {
        for (var i = 0; i < data.length; i++) {
            var course = data[i];
            if(course.position.x == position.x && course.position.y == position.y) {
                return course;
            }
        }
        return null;
    }

    function init_grid($studyplan, data, year) {
        var data_year = year_data(data, year);
        var num_rows = find_greatest_y(data_year) + 1; // +1 Because we like to palayey

        for (var i = 0; i < num_rows; i++) {
            var $tr = $("<tr></tr>");
            for (var j = 0; j < 4; j++) {
                var $td = $("<td class='td_course'>").droppable();
                var itd = init_td($tr.children("td").length, i);
                $td.data(itd);
                $tr.append($td);
            }
            $studyplan.append($tr);
        }
    }


    function find_greatest_y(data) {
        var max = 0;
        data.forEach(function (course) {
            if (course.position.y > max) {
                max = course.position.y;
            }
        })
        return max + 1;
    }

    function find_rows_num(data, year) {
        var prev_period = null;
        var max_rows = 0;
        var period_rows = 1;
        data.forEach(function (course) {
            var course_period = parseInt(course["period"].substring(1,2));
            var course_year = parseInt(course["period"].substring(0,1));
            if (year === course_year) {
                if (course_period == prev_period) {
                    period_rows++;
                }
                else {
                    period_rows = 1;
                }
                if (period_rows > max_rows) {
                    max_rows = period_rows;
                }
            }

            prev_period = course_period;
        });
        return max_rows;
    }

    function manage_data(data) {
        data.sort(function (a, b) {
        var period_a = parseInt(a.period);
        var period_b = parseInt(b.period);

        if (period_a < period_b) return -1;
        if (period_a > period_b) return 1;
        return 0;
        });
        data.forEach(function (course){
            var occurrence = 0;
            var course_code = course.code;
            for(var i = 0; i < data.length; i++){
                if(data[i].code == course_code){
                    occurrence++;
                    if(occurrence > 1){
                        course.dup = true;
                        course.credits = course.credits + " " + data[i].credits;
                        data.splice(i, 1);
                    }
                }
            }
        });
    }

    $(".course").draggable({
        snap: false,
        cursor: "move",
        revert: "invalid"
    });

    function event_expand(){
        $course = $(this).parent();
        if($course.hasClass("extend")){ //From double to single
            $course.toggleClass("extend");
            $(this).toggleClass("rotated");
            $course.data().course.dup = false;
            $course.parent().next().data("free", true);
        }
        else{   // From single to double
            if($course.parent().next().data("free")){
                $course.toggleClass("extend");
                $(this).toggleClass("rotated");
                $course.data().course.dup = true;
                $course.parent().next().data("free", false);
            }
            else{
                $course.effect("shake", {distance: 10, times:2}, 300);
            }
        }
        event.stopPropagation();
        sync_data();
    }

    function event_dragstart(event, ui) {
        var parent = $(this).parent(".td_course");
        var course = $(this).data("course");
        $(this).css("z-index", "100").css("opacity", "0.7");
        drop_help(parent, course.dup, true);
    }

    function event_dragstop(event, ui){
        var parent = $(this).parent(".td_course");
        var course = $(this).data("course");
        $(this).css("z-index", "1").css("opacity", "1").removeClass("warning");
        drop_help(parent, course.dup, false);
    }
    $(".course").on("dragstop", event_dragstop).on("dragstart", event_dragstart);
    $(".expandCourse").on("click", event_expand);

    function drop_help(target, dup, free) {
        target.data("free", free);
        if (dup === true) {
            target.next().data("free", free);
        }
    }

    function sync_data() {
        var d = [];
        $(".course").each(function() {
            if($(this).data("course").period)
                d.push($(this).data("course"));
        });
        data = d;
        localStorage.setItem("synced_data", JSON.stringify(d));
    }

    function needs_another_row(table, y) {
        var $table = $(table);
        return (y+1) == ($table.find("tr").length -1);
    }

    function add_table_row(table, y) {
        y++;
        var $table = $(table);
        var $tr = $("<tr></tr>");
         for (var j = 0; j < 4; j++) {
            var $td = $("<td class='td_course'>").droppable({
                        accept: ".course",
                        tolerance: "pointer"
                    }).on("drop", drop_event)
                    .on("dropover", dropover_event)
                    .on("dropout", dropout_event);
            var itd = init_td($tr.children("td").length, y);
            $td.data(itd);
            $tr.append($td);
        }
        $table.append($tr);
    }

    function dropout_event(event, ui){
        var course_data = ui.draggable.data("course");
            $(this).removeClass("highlighted");
            if(course_data.dup){
                $(this).next().removeClass("highlighted");
            }
    };

    function dropover_event(event, ui){
        var course_data = ui.draggable.data("course");
        $(this).addClass("highlighted");
        if(course_data.dup){
            $(this).next().addClass("highlighted");
        }
        if(!$(this).data("free")){
            ui.draggable.addClass("warning");
        }
        else{
            ui.draggable.removeClass("warning");
        }
        if(course_data.dup && (($(this).data().x === 3) || !$(this).next().data("free"))){
            ui.draggable.addClass("warning");
        }
    };

    function last_row_empty($studyplans) {
        $studyplans.each(function (index, studyplan) {
            var data_year = year_data(data, index+1);
            var $studyplan = $(studyplan);
            var $trs = $studyplan.find("tr");
            var max_y = find_greatest_y(data_year) + 1;
            var trs_length = $trs.length -1;
            while (max_y < trs_length) {
                trs_length--;
                $trs.last().remove();
                $trs = $studyplan.find("tr");
            }
        });
    }

    function drop_event(event, ui) {
        var data = $(this).data();
        var draggable_data = ui.draggable.data("course");
        var parent = ui.draggable.parent(".td_course");
        var next_free = $(this).next().data("free");

        ui.draggable.removeClass("warning");
        $(this).removeClass("highlighted");

        if(draggable_data.dup){
            $(this).next().removeClass("highlighted");
        }

        $element = ui.draggable.css("left", 0).css("top", 0);
        if(data.free === true && !(draggable_data.dup === true && (data.x === 3 || !next_free))) {
            var table = $(this).parent().parent().parent()[0];
            var position = {x: data.x, y: data.y};
            $(this).append($element);
            drop_help($(this), draggable_data.dup, false);
            drop_help(parent, draggable_data.dup, true);
            draggable_data.position = position;
            draggable_data.period = table.getAttribute("data-year") + String(data.x+1);
            sync_data();
            needs_another_row(table, position.y) && add_table_row(table, position.y);
            last_row_empty($studyplans);
        }
    }

    $(".td_course").droppable({
        accept: ".course",
        tolerance: "pointer"
    }).on("drop", drop_event).on("dropover", dropover_event).on("dropout", dropout_event);

    function event_click(){
        var course = $(this).data().course;
        $('.focused').removeClass("focused");
        $(this).addClass("focused");
        $(".course-information").find(".course_header").html("<a target='_blank' href=http://www.uu.se/utbildning/utbildningar/selma/kursplan/?kKod="+ course.code +">" + course.name + "</a>" );
        $(".course-information").find(".course_hp").html("HP: "+ course.credits);
        $(".course-information").find(".course_level").html("Nivå: " +course.level);
        $(".course-information").find(".course_code").html("Kurskod: "+ course.code);
    }

    function event_remove(){
        var course = $(this).parent();
        drop_help(course.parent(), course.data().course.dup, true);
        course.remove();
        sync_data();
    }

    $(".removeCourse").on("click", event_remove);
    $(".course").on("click", event_click);

    $(".dropdown").click(function(){
        $(this).next().toggle();
        $(this).children("img").toggleClass("rotated");
    });

    function spawnCourse(data){
        var $course = $("<div class='course'><div class='removeCourse'></div><div class='expandCourse'></div><div>" + data.kurskod + "  " + data.niva + " <strong>" + data.poang +"HP</strong> <br>" + data.namn + "</div></div>");
        $course.draggable({
                snap: false,
                cursor: "move",
                revert: "invalid"
            });
        $course.on("dragstart", event_dragstart);
        $course.on("dragstop", event_dragstop);
        $course.on("click", event_click);
        $course.find(".removeCourse").on("click", event_remove);
        $course.find(".expandCourse").on("click", event_expand);
        var datum = {
            code: data.kurskod,
            level: data.nivå,
            credits: data.poang,
            name: data.namn,
            period: null,
            position: {
                x: null,
                y: null
            },
            dup: false
        }
        $course.data("course", datum);
        $course.addClass(course_class(data.kurskod));
        $("#spawnCourse").html($course);
    };
    $( ".search-course" ).autocomplete({
      source: function(request, response){
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "http://127.0.0.1:8000/coursefy/api/courses/"+request.term,
            success: function(data){
                response($.map(data, function(item) {
                    return {
                        label: item.kurskod,
                        data: item
                    }
                }));
            }
        });
      },
      select: function(event, ui){
        spawnCourse(ui.item.data);
      }
    });
});
