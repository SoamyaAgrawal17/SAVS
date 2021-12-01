var login_email_id = "no id";
var global_url = "http://localhost:5000/";

function student_login(email){
    var xhr = new XMLHttpRequest();
    var url = global_url + "student/" + email;
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            var json = JSON.parse(xhr.responseText);
            console.log(json)
            if (json != "Student does not exist"){
                document.getElementById("information-container").style.display = "block"
                document.getElementById("login-form").innerHTML = "<h5>Welcome " + email + "</h5>"
                login_email_id = email;
            }
            else{
                document.getElementById("login-form").innerHTML = "<h5>" + json + "</h5>"
            }
        }else{
            console.log("here");
        }
    };
    xhr.send();
}

function get_club_by_id(club_id){
    var xhr = new XMLHttpRequest();
    var url = global_url + "clubs/" + club_id;
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            var json = JSON.parse(xhr.responseText);
            console.log(json)
            if (json == null){
                document.getElementById("club-id-found").style.display = "none"
                document.getElementById("club-id-not-found").style.display = "inline"
            }else{
                document.getElementById("club-id-found").style.display = "inline"
                document.getElementById("club-id-not-found").style.display = "none"

                club_name = json.name;
                club_head = json.head;
                club_category = json.category;
                club_description = json.description;

                document.getElementById("club-id-found-id").innerHTML = "Club ID: " + club_id;
                document.getElementById("club-id-found-name").innerHTML = "Club Name: " + club_name;
                document.getElementById("club-id-found-head").innerHTML = "Club Head: " + club_head;
                document.getElementById("club-id-found-category").innerHTML = "Club Category: " + club_category;
                document.getElementById("club-id-found-description").innerHTML = "Club Description: " + club_description;
            }
        }else{
            console.log("here");
        }
    };
    xhr.send();
}

function get_event_by_id(event_id){
    var xhr = new XMLHttpRequest();
    var url = global_url + "events/" + event_id;
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            var json = JSON.parse(xhr.responseText);
            console.log(json)
            if (json == null){
                document.getElementById("event-id-found").style.display = "none"
                document.getElementById("event-id-not-found").style.display = "inline"
            }else{
                document.getElementById("event-id-found").style.display = "inline"
                document.getElementById("event-id-not-found").style.display = "none"

                event_name = json.name;
                event_description = json.description;
                event_location = json.location;
                event_start = json.start_timestamp;
                event_end = json.end_timestamp;
                event_category = json.category;

                document.getElementById("event-id-found-id").innerHTML = "Event ID: " + event_id;
                document.getElementById("event-id-found-name").innerHTML = "Event Name: " + event_name;
                document.getElementById("event-id-found-description").innerHTML = "Event Description: " + event_description;
                document.getElementById("event-id-found-location").innerHTML = "Event Location: " + event_location;
                document.getElementById("event-id-found-start").innerHTML = "Event Start: " + event_start;
                document.getElementById("event-id-found-end").innerHTML = "Event End: " + event_end;
                document.getElementById("event-id-found-category").innerHTML = "Event Category: " + event_category;
            }
        }else{
            console.log("here");
        }
    };
    xhr.send();
}

function create_club(){
    var xhr = new XMLHttpRequest();
    var url = global_url + "student/club";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            document.getElementById("create-club-response").style.display = "inline";
            document.getElementById("create-club-response").innerHTML = json;
        }else{
            var json = JSON.parse(xhr.responseText);
            document.getElementById("create-club-response").style.display = "inline";
            document.getElementById("create-club-response").innerHTML = json;
        }
    };
    var data = JSON.stringify({
        "emailId":login_email_id,
        "club":{
            "name": document.getElementById("create-club-name").value,
            "head": document.getElementById("create-club-head").value,
            "category": document.getElementById("create-club-category").value,
            "description": document.getElementById("create-club-description").value,
        }
    });
    xhr.send(data);
}

function get_all_clubs(){
    var xhr = new XMLHttpRequest();
    var url = global_url + "clubs";
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            console.log(json)
            if (json.length>0){
                var innerHTML = ""
                for (let i = 0; i < json.length; i++) {
                    innerHTML = innerHTML + `<div class="row">
                                        <div class="col-12">
                                        <div class="row">Club ID: `+json[i]._id+`</div>
                                        <div class="row">Club Name: `+json[i].name+`</div>
                                        <div class="row">Club Head: `+json[i].head+`</div>
                                        <div class="row">Club Category: `+json[i].category+`</div>
                                        <div class="row">Club Description: `+json[i].description+`</div>
                                    </div>
                                </div><br>`
                  }
                document.getElementById("all-clubs-information").innerHTML = innerHTML;
            }else{
                // No clubs found
                document.getElementById("all-clubs-information").innerHTML = "No Clubs in the database";
            }
        }else{
            console.log("here");
        }
    };
    xhr.send();
}

function add_member(){
    var xhr = new XMLHttpRequest();
    var url = global_url + "member/" + document.getElementById("member-club-id").value;
    xhr.open("PUT", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = xhr.responseText;
            console.log(json)
            document.getElementById("add-member-response").innerHTML = json;
        }else{
            console.log("here");
            var json = xhr.responseText;
            console.log(json)
            document.getElementById("add-member-response").innerHTML = json;
        }
    };
    var data = JSON.stringify({
        "emailId":login_email_id,
        "student_email_id":document.getElementById("member-id").value
    })
    xhr.send(data);   
}

function delete_club(){
    var xhr = new XMLHttpRequest();
    var url = global_url + "clubs/" + document.getElementById("delete-club-id").value;
    xhr.open("DELETE", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = xhr.responseText;
            console.log(json)
            document.getElementById("delete-club-response").innerHTML = json;
        }else{
            console.log("here");
            var json = xhr.responseText;
            console.log(json)
            document.getElementById("delete-club-response").innerHTML = json;
        }
    };
    var data = JSON.stringify({
        "emailId":login_email_id
    })
    xhr.send(data); 
}

function get_roles(){
    var xhr = new XMLHttpRequest();
    var url = global_url + "student/get_roles";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            if (json.length>0){
                var innerHTML = ""
                for (let i = 0; i < json.length; i++) {
                    innerHTML = innerHTML + `<div class="row">
                                        <div class="col-12">
                                        <div class="row">Club ID: `+json[i].club_id+`</div>
                                        <div class="row">Role: `+json[i].role+`</div>
                                    </div>
                                </div><br>`
                  }
                document.getElementById("get-roles-response").innerHTML = innerHTML;
            }else{
                // No clubs found
                document.getElementById("get-roles-response").innerHTML = "Not registered in any clubs";
            }
        }else{
            console.log("here");
            var json = xhr.responseText;
            console.log(json)
            // document.getElementById("get-roles-response").innerHTML = json;
        }
    };
    var data = JSON.stringify({"emailId":login_email_id});
    xhr.send(data); 
}

// EVENTS

function create_event(){
    var xhr = new XMLHttpRequest();
    var url = global_url + "/events";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 201) {
//            var json = JSON.parse(xhr.responseText);
            var json = xhr.responseText;
            console.log(json)
            document.getElementById("create-event-response").style.display = "inline";
            document.getElementById("create-event-response").innerHTML = json;
        }else{
//            var json = JSON.parse(xhr.responseText);
            var json = xhr.responseText;
            console.log(json)
            document.getElementById("create-event-response").style.display = "inline";
            document.getElementById("create-event-response").innerHTML = json;
        }
    };
    var data = JSON.stringify({
        "emailId":login_email_id,
        "event":{
            "name": document.getElementById("create-event-name").value,
            "club_id": parseInt(document.getElementById("create-event-club-id").value),
            "start_timestamp": document.getElementById("create-event-start-timestamp").value,
            "end_timestamp": document.getElementById("create-event-end-timestamp").value,
            "location": document.getElementById("create-event-location").value,
            "max_registration": parseInt(document.getElementById("create-event-max-registration").value),
            "description": document.getElementById("create-event-description").value,
            "fee": parseInt(document.getElementById("create-event-fee").value),
            "category": document.getElementById("create-event-category").value,
            "visibility": document.getElementById("create-event-visibility").value,

        }
    });
    xhr.send(data);
}
