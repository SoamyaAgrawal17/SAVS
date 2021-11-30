var login_email_id = "no id";
var global_url = "http://localhost:5000/";

function student_login(email){
    var xhr = new XMLHttpRequest();
    var url = global_url + "/student/" + email;
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
    var url = global_url + "/clubs/" + club_id;
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
                event_location = json.event_location;
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
