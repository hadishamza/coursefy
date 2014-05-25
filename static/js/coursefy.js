var coursefy = {
    data: [],
    uuid: null,
    parent_id: 0,
    course_data: [],
    $studyplans: [],

    initialize: function($studyplans) {
        var self = this;
        this.$studyplans = $studyplans;
        if (!self.uuid && !self.parent_id) {
            self.manage_data(self.data);

        }
        else {
            self.course_data = self.data;
        }
        $studyplans.each(function(index, studyplan) {
            if (!self.uuid && !self.parent_id){
                self.init_studyplan_pos(self.data, index+1);
            }


            self.init_grid($(studyplan), self.course_data, index+1);
            self.populate_studyplan($(studyplan), self.course_data, index+1);
        });
        self.course_data = null;
        self.data = null;
    },

    /***** DRAW METHODS BEGIN *****/
    $td_course: function(x, y, free) {
        var data = this.init_td(x,y, free);
        return $("<td class='td_course'>").droppable({
            accept: ".course",
            tolerance: "pointer"
        }).on("drop", this.drop_event)
        .on("dropover", this.dropover_event)
        .on("dropout", this.dropout_event)
        .data(data);
    },

    init_td: function (x, y, free) {
        free = (typeof free === "undefined") ? true : free;
        return {x: x, y: y, free: free};
    },

    $course: function(data) {
        var $course = $("<div class='course'><div class='removeCourse'></div><div class='expandCourse'></div><div>" + data["code"] + "  " + data["level"] + " <strong>" + data["credits"] +"HP</strong> <br>" + data["name"] + " </div></div>");

        $course.draggable({
            snap: false,
            //cursorAt: {top: 25, left: 25},
            cursor: "move",
            revert: "invalid"
        }).on("dragstop", this.event_dragstop).on("dragstart", this.event_dragstart).on("click", this.event_click);
        $course.on("mouseover", coursefy.mouseover_event)
        .on("mouseleave", coursefy.mouseleave_event);
        $course.find(".removeCourse").on("click", this.event_remove);
        $course.find(".expandCourse").on("click", this.event_expand);
        $course.data("course", data);
        $course.css("background-color",this.course_class(data.level));
        return $course;
    },

    spawnCourse: function (data){
        data.position = {
                x: null,
                y: null
            };
        var $course = this.$course(data);
        $("#spawnCourse").html($course);
    },

    init_grid: function ($studyplan, data, year) {
        var data_year = this.year_data(data, year);
        var num_rows = this.find_greatest_y(data_year) + 1; // +1 Because we like to palayey
        for (var i = 0; i < num_rows; i++) {
            var $tr = $("<tr></tr>");
            for (var j = 0; j < 4; j++) {
                var $td = this.$td_course($tr.children("td").length, i);
                $tr.append($td);
            }
            $studyplan.append($tr);
        }
    },

    course_class: function (course_level) {
        var type_class;
        switch(course_level) {
            case "G1N":
                type_class = "#d0ebff";
                break;
            case "G1F":
                type_class = "#92d2ff";
                break;
            case "G2F":
                type_class = "#5aabe5";
                break;
            case "G2E":
                type_class = "#4685b2";
                break;

            case "A1N":
                type_class = "#b7f3cc";
                break;
            case "A1F":
                type_class = "#8cecad";
                break;
            case "A2F":
                type_class = "#70e899";
                break;
            case "A2E":
                type_class = "#59b97a";
                break;
            default:
                type_class = "#FF9E8E";
                break;
        }

        return type_class;
    },

    table_structure: function (years){
        for(var i = 1; i <= years; i++){
            $(".main-table").append("<h2>År "+ i +"</h2>");
            $tableElem = $("<table data-year=" + i +" class='studyplan table table-bordered'>");
            $(".main-table").append($tableElem);
            $theadElem = $("<thead>");
            $tableElem.append($theadElem);
            $theadTrElem = $("<tr>");
            $theadElem.append($theadTrElem);
            $thElem = $("<th>Period 1</th><th>Period 2</th><th>Period 3</th><th>Period 4</th>")
            $theadTrElem.append($thElem);
            $tableElem.append("<tbody>");
        }
    },

    /***** DRAW METHODS END *****/

    year_data: function (data, year){
        var data_year = [];
        data.forEach(function (course) {
            if (course["period"] == 0) {
            }
            var course_year = parseInt(String(course["period"]).substring(0,1));
            if (course_year === year) {
                data_year.push(course);
            }
        });
        return data_year;
    },

    init_studyplan_pos: function (data, year) {
        var data_year = this.year_data(data, year);
        var num_rows = this.find_rows_num(data_year, year);
        var start_period = 1+(year*10);
        var i;
        for (i = 0; i < num_rows; i++) {
            var k = 0;
            for (var period = start_period; period <= (start_period+3); period++) {
                var extended;
                for(var j = 0; j < data_year.length; j++) {
                    extended = false;
                    var course = data_year[j];
                    var course_period = parseInt(course["period"]);
                    if (course_period === period) {
                        data_year.splice(j, 1);
                        if (!course.position)
                            course.position = {x: k, y: i};

                        if (course.extended){
                            period++;
                            k++;
                        }
                        this.course_data.push(course);
                        break;
                    }
                }
                k++;
            }
        }
    },

    populate_studyplan: function ($studyplan, data, year) {
        var data_year = this.year_data(data, year);
        var num_rows = this.find_greatest_y(data_year);
        var self = this;
        $studyplan.find("tbody > tr").each(function(y) {
            var $tr = $(this);
            $tr.children("td").each(function(x) {
                var $td = $(this);
                var position = {x:$td.data("x"), y:$td.data("y")};
                var course = self.find_course_by_pos(data_year, position);
                if (course) {
                    var $course = self.$course(course);
                    $td.html($course);

                    self.drop_help($td, course.extended, false);
                    if(course.extended) {
                        $course.find(".expandCourse").addClass("rotated");
                        $course.addClass("extend");
                    }
                }
            });
        });
    },

    find_course_by_pos: function (data, position) {
        for (var i = 0; i < data.length; i++) {
            var course = data[i];
            if(course.position.x == position.x && course.position.y == position.y) {
                return course;
            }
        }
        return null;
    },

    find_greatest_y: function (data) {
        var max = 0;
        data.forEach(function (course) {
            if (course.position.y > max) {
                max = course.position.y;
            }
        });
        return max + 1;
    },

    number_of_years: function (data) {
        var max = 0;
        data.forEach(function (course) {
            year = Math.floor(course.period/10);
            if (year > max)
                max = year;
        });
        return max;
    },

    /***** TABLE HELPERS BEGIN *****/
    needs_another_row: function (table, y) {
        var $table = $(table);
        return (y+1) == ($table.find("tr").length -1);
    },

    add_table_row: function (table, y) {
        var self = this;
        y++;
        var $table = $(table);
        var $tr = $("<tr></tr>");
         for (var j = 0; j < 4; j++) {
            var $td = self.$td_course($tr.children("td").length, y);
            $tr.append($td);
        }
        $table.append($tr);
    },

    last_row_empty: function () {
        var self = this;
        this.$studyplans.each(function (index, studyplan) {
            var data_year = self.year_data(data, index+1);
            var $studyplan = $(studyplan);
            var $trs = $studyplan.find("tr");
            var max_y = self.find_greatest_y(data_year) + 1;
            var trs_length = $trs.length -1;
            while (max_y < trs_length) {
                trs_length--;
                $trs.last().remove();
                $trs = $studyplan.find("tr");
            }
        });
    },

    find_rows_num: function (data, year) {
        var prev_period = null;
        var max_rows = 0;
        var period_rows = 1;
        this.data.forEach(function (course) {
            var course_period = parseInt(String(course["period"]).substring(1,2));
            var course_year = parseInt(String(course["period"]).substring(0,1));
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
    },

    /***** TABLE HELPERS END *****/

    manage_data: function (data) {
        data.sort(function (a, b) {
        var period_a = parseInt(a.period);
        var period_b = parseInt(b.period);

        if (period_a < period_b) return -1;
        if (period_a > period_b) return 1;
        return 0;
        });
    },

    /***** EVENTS BEGIN *****/

    event_expand: function (){
        var $course = $(this).parent();
        if($course.hasClass("extend")){ //From double to single
            $course.toggleClass("extend");
            $(this).toggleClass("rotated");
            $course.data().course.extended = false;
            $course.parent().next().data("free", true);
        }
        else{   // From single to double
            if($course.parent().next().data("free")){
                $course.toggleClass("extend");
                $(this).toggleClass("rotated");
                $course.data().course.extended = true;
                $course.parent().next().data("free", false);
            }
            else{
                $course.effect("shake", {distance: 10, times:2}, 300);
            }
        }
        event.stopPropagation();
        coursefy.sync_data();
    },

    event_dragstart: function (event, ui) {
        var parent = $(this).parent(".td_course");
        var course = $(this).data("course");
        $(this).css("z-index", "100").css("opacity", "0.7");
        coursefy.drop_help(parent, course.extended, true);
    },

    event_dragstop: function (event, ui){
        var parent = $(this).parent(".td_course");
        var course = $(this).data("course");
        $(this).css("z-index", "1").css("opacity", "1").removeClass("warning");
        coursefy.drop_help(parent, course.extended, false);
    },

    dropout_event: function (event, ui){
        var course_data = ui.draggable.data("course");
            $(this).removeClass("highlighted");
            if(course_data.extended){
                $(this).next().removeClass("highlighted");
            }
    },

    dropover_event: function (event, ui){
        var course_data = ui.draggable.data("course");
        $(this).addClass("highlighted");
        if(course_data.extended){
            $(this).next().addClass("highlighted");
        }
        if(!$(this).data("free")){
            ui.draggable.addClass("warning");
        }
        else{
            ui.draggable.removeClass("warning");
        }
        if(course_data.extended && (($(this).data().x === 3) || !$(this).next().data("free"))){
            ui.draggable.addClass("warning");
        }
    },

    event_click: function (){
        var course = $(this).data().course;
        $('.focused').removeClass("focused");
        $(this).addClass("focused");
        $(".course-information").find(".course_header").html("<a target='_blank' href=http://www.uu.se/utbildning/utbildningar/selma/kursplan/?kKod="+ course.code +">" + course.name + "</a>" );
        $(".course-information").find(".course_hp").html("HP: "+ course.credits);
        $(".course-information").find(".course_level").html("Nivå: " +course.level);
        $(".course-information").find(".course_code").html("Kurskod: "+ course.code);
        $(".course-information").find(".course_requirements").html("<h4>Behörighet</h4> "+ course.requirements)
        $(".course-information").find(".course_examination").html("<h4>Examination</h4> "+ course.examination)
    },

    event_remove: function (){
        var course = $(this).parent();
        coursefy.drop_help(course.parent(), course.data().course.extended, true);
        course.remove();
        coursefy.sync_data();
    },

    drop_event: function (event, ui) {
        var data = $(this).data();
        var draggable_data = ui.draggable.data("course");
        var parent = ui.draggable.parent(".td_course");
        var next_free = $(this).next().data("free");

        ui.draggable.removeClass("warning");
        $(this).removeClass("highlighted");

        if(draggable_data.extended){
            $(this).next().removeClass("highlighted");
        }

        $element = ui.draggable.css("left", 0).css("top", 0);
        if(data.free === true && !(draggable_data.extended === true && (data.x === 3 || !next_free))) {
            var table = $(this).parent().parent().parent()[0];
            var position = {x: data.x, y: data.y};
            $(this).append($element);
            coursefy.drop_help($(this), draggable_data.extended, false);
            coursefy.drop_help(parent, draggable_data.extended, true);
            draggable_data.position = position;
            draggable_data.period = table.getAttribute("data-year") + String(data.x+1);
            coursefy.sync_data();
            coursefy.needs_another_row(table, position.y) && coursefy.add_table_row(table, position.y);
            coursefy.last_row_empty();
        }
    },

    mouseover_event: function(){
        $(this).find(".removeCourse").css("visibility", "visible");
        $(this).find(".expandCourse").css("visibility", "visible");
    },

    mouseleave_event: function(){
        $(this).find(".removeCourse").css("visibility", "hidden");
        $(this).find(".expandCourse").css("visibility", "hidden");
    },

    /***** EVENTS END *****/
    drop_help: function (target, extended, free) {
        target.data("free", free);
        if (extended === true) {
            target.next().data("free", free);
        }
    },

    sync_data: function () {
        var d = [];
        var self = this;
        var post_data;
        var base_url = "/coursefy/default/studyplan/";
        $(".course").each(function() {
            if($(this).data("course").period)
                d.push($(this).data("course"));
        });
        data = d;

        if (self.uuid == null) {
            post_data = {"parent_id": this.parent_id, "user_studyplan": JSON.stringify(data)};
            $.ajax({
                type: "POST",
                dataType: "json",
                data: post_data,
                url: "/coursefy/api/user_studyplan/"
            })
            .done(function(data) {
                self.uuid = data.uuid;
                window.history.pushState(null, null, base_url+self.uuid);
            })
            .fail(function() {
            });
        }
        else {
            post_data = {"key": self.uuid, "user_studyplan": JSON.stringify(data)};
            $.ajax({
                type: "PUT",
                dataType: "json",
                data: post_data,
                url: "/coursefy/api/user_studyplan/"
            })
            .done(function(data) {
            })
            .fail(function() {
            });
        }
    }
}


$( document ).ready(function() {
    /** Hood router BEGIN **/
    var URL = window.location.pathname.split("/");
    var last = URL[URL.length-1];
    var second_last = URL[URL.length-2];
    var years = 0;

    if (second_last == "new") {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/coursefy/api/studyplan/"+last
        })
        .done(function(data) {
            coursefy.data = data;
            years = coursefy.number_of_years(data);
            coursefy.table_structure(years);
            coursefy.initialize($(".studyplan"));
            return true;
        })
        .fail(function() {
            return null;
        });
    }
    else if (last.length == 36){ // UUID
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/coursefy/api/user_studyplan/"+last
        })
        .done(function(data) {
            coursefy.data = data.value;
            years = coursefy.number_of_years(data.value);
            coursefy.table_structure(years);
            coursefy.parent_id = last;
            coursefy.initialize($(".studyplan"));
            return true;
        })
        .fail(function() {
            return null;
        });
    }
    else {
        window.location = "/coursefy/default/"
    }
    /** Hood router END **/

    $(".dropdown").click(function(){
        $(this).next().toggle();
        $(this).children("img").toggleClass("rotated");
    });
    $(".course")
    .on("mouseover", coursefy.mouseover_event)
    .on("mouseleave", coursefy.mouseleave_event);

    $( ".search-course" ).autocomplete({
        minLength: 3,
        source: function(request, response){
            $.ajax({
                type: "GET",
                dataType: "json",
                url: "http://127.0.0.1:8000/coursefy/api/courses/"+request.term
            })
            .done(function(data){
                response($.map(data, function(item) {
                    return {
                        label: item.code + " - " + item.name,
                        data: item
                    }
                }));
            })
            .fail(function( jqXHR, textStatus ) {
                // Todo handle error here
            });
        },
        select: function(event, ui){
            coursefy.spawnCourse(ui.item.data);
        }
    });
});
