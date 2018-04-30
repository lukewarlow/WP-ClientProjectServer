var enhanced_services = [];

let serviceMap = new Map();

function submitAddForm()
{
    var form = document.forms["addPharmacy"];
    var name = form["name"].value;
    var lat = form["lat"].value;
    var long = form["long"].value;

    var phoneNumber = form["phoneNumber"].value;

    var welshAvailable = form["welshAvailable"].checked;

    var openingTimes = "";

    var mondayOpen = form["mondayOpen"].value;
    var mondayClose = form["mondayClose"].value;
    openingTimes += mondayOpen + ":" + mondayClose + ",";

    var tuesdayOpen = form["tuesdayOpen"].value;
    var tuesdayClose = form["tuesdayClose"].value;
    openingTimes += tuesdayOpen + ":" + tuesdayClose + ",";

    var wednesdayOpen = form["wednesdayOpen"].value;
    var wednesdayClose = form["wednesdayClose"].value;
    openingTimes += wednesdayOpen + ":" + wednesdayClose + ",";

    var thursdayOpen = form["thursdayOpen"].value;
    var thursdayClose = form["thursdayClose"].value;
    openingTimes += thursdayOpen + ":" + thursdayClose + ",";

    var fridayOpen = form["fridayOpen"].value;
    var fridayClose = form["fridayClose"].value;
    openingTimes += fridayOpen + ":" + fridayClose + ",";

    var saturdayOpen = form["saturdayOpen"].value;
    var saturdayClose = form["saturdayClose"].value;
    openingTimes += saturdayOpen + ":" + saturdayClose + ",";

    var sundayOpen = form["sundayOpen"].value;
    var sundayClose = form["sundayClose"].value;
    openingTimes += sundayOpen + ":" + sundayClose;

    var enhancedServices = "";
    for (var entry of serviceMap.entries())
    {
        var index = entry[0].id;
        enhancedServices += entry[1] + ",";
    }
    enhancedServices = enhancedServices.substr(0, enhancedServices.length - 1);

    var pin = form["pincode"].value;
    var params = 'name=' + htmlEntities(name) + '&lat=' + lat + '&long=' + long + '&phoneNumber=' + phoneNumber + '&welshAvailable=' + welshAvailable + '&openingTimes=' + openingTimes + "&services=" + enhancedServices + '&pincode=' + pin;
    var xhttp = new XMLHttpRequest();
    var msg = "";
    xhttp.open("post", "/addpharmacy", true); // true is asynchronous
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function ()
    {
        if (xhttp.readyState === 4)
        {
            if (xhttp.status === 200)
            {
                msg = xhttp.responseText;
                if (msg === "Invalid pin code")
                    document.getElementById("pincode").style.border = "3px solid red";
                else
                {
                    form.reset();
                    document.getElementById("pincode").style.border = "none";
                }
                document.getElementById("response").innerText = msg;
            }
            else
            {
                console.error(xhttp.statusText);
                msg = "Error: other wierd response " + xhttp.status;
            }
            console.log(msg);
        }
    };
    xhttp.send(params);

    return false;
}

function submitDeleteForm()
{
    var form = document.forms["deletePharmacy"];
    var name = form["name"].value;
    var phoneNumber = form["phoneNumber"].value;
    var pin = form["pincode"].value;

    var params = 'name=' + name + '&phoneNumber=' + phoneNumber + '&pincode=' + pin;
    var xhttp = new XMLHttpRequest();
    var msg = "";
    xhttp.open("DELETE", "/deletepharmacy", true); // true is asynchronous
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function ()
    {
        if (xhttp.readyState === 4)
        {
            if (xhttp.status === 200)
            {
                msg = xhttp.responseText;
                if (msg === "Invalid pin code")
                    document.getElementById("pincode").style.border = "3px solid red";
                else if (msg === "Record successfully deleted.")
                {
                    form.reset();
                    document.getElementById("pincode").style.border = "none";
                }
                document.getElementById("response").innerText = msg;
            }
            else
            {
                console.error(xhttp.statusText);
                msg = "Error: other wierd response " + xhttp.status;
            }
            console.log(msg);
        }
    };
    xhttp.send(params);

    return false;
}

function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function loadOptions(services)
{
    enhanced_services = services
    enhanced_services.unshift("none")
    divToChange = document.getElementById("newServiceSection1");
    divToChange.innerHTML = `
    <h3>Select which enhanced services are available.</h3>
    <div id="service1">
        <div id="serviceSelect1">
            <label for="service">Please select a service: </label>
            <select name="service" id="1" onchange="serviceSelected(this)">`;
    let serviceDiv = document.getElementById("1");
    for (var i = 0; i < enhanced_services.length; i++)
    {
        let text = enhanced_services[i].replace('_', ' ').replace('_', ' ').replace('_', ' ');
        text = text.capitalize();
        serviceDiv.innerHTML += `"<option value=` + enhanced_services[i] + `>` + text + `</option>"`;
    }

    divToChange.innerHTML += `</select>
        </div>
    </div>
    <br>
    <br>
    <div id="newServiceSection2"></div>`;
}

function serviceSelected(selectbox)
{
    if (serviceMap.size < enhanced_services.length - 2)
    {
        if (selectbox.value !== "none")
        {
            serviceMap.set(selectbox, selectbox.value);
            index = selectbox.id
            index++;
            var divToChange = document.getElementById("newServiceSection" + index);
            divToChange.innerHTML = `
                <div id="service` + index + `">
                    <div id="serviceSelect` + index + `">
                        <label for="service">Please select a service: </label>
                        <select name="service" id="` + index + `" onchange="serviceSelected(this)">`;

            let serviceDiv = document.getElementById(index);
            for (var i = 0; i < enhanced_services.length; i++)
            {
                if (!valueInMap(serviceMap, enhanced_services[i]))
                {
                    let text = enhanced_services[i].replace('_', ' ').replace('_', ' ').replace('_', ' ');
                    text = text.capitalize();
                    serviceDiv.innerHTML += `"<option value=` + enhanced_services[i] + `>` + text + `</option>"`;
                }
            }

            divToChange.innerHTML += `</select>
                    </div>
                </div>
                <br>
                <br>
                <div id="newServiceSection` + (index + 1).toString() + `"></div>`;
        }
    }
}

function valueInMap(map, text)
{
    var found = false;
    for (var entry of map.entries())
    {
        if (entry[1] === text)
        {
            found = true;
            break;
        }
    }
    return found;
}

String.prototype.capitalize = function ()
{
    return this.replace(/(^|\s)([a-z])/g, function (m, p1, p2)
    {
        return p1 + p2.toUpperCase();
    });
};