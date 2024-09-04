const menuBtn = document.querySelector(".header-mobile-button");
const mobileMenu = document.querySelector(".mobile-menu");

menuBtn.addEventListener("click", function () {
  menuBtn.classList.toggle("active");
  mobileMenu.classList.toggle("active");
});

window.addEventListener("scroll", function () {
  var header = document.querySelector(".header");
  if (window.scrollY > 0) {
    header.classList.add("header-scrolled");
  } else {
    header.classList.remove("header-scrolled");
  }
});


const dashboardBtn = document.querySelector(".sidebar-show-icon");
const dashboardMenu = document.querySelector(".category-container");
const dashboardBtnIcon = document.querySelector(".sidebar-show-icon-icon");
const dashboardSidebar = document.querySelector(".sidebar");

dashboardBtn.addEventListener("click", function () {
  dashboardBtnIcon.classList.toggle("active");
  dashboardMenu.classList.toggle("active");
  dashboardSidebar.classList.toggle("active");
});

const sportBtn = document.getElementsByClassName("sport");
const sportIcon = document.getElementsByClassName("sport-icon");
const sportContent = document.getElementsByClassName("sport-content");
console.log(sportBtn[4])
console.log(sportContent[4])
for(var i=0;i<sportBtn.length;i++)
{

  (function(index) { // Create a closure to capture the current value of i
    sportBtn[index].addEventListener("click", function () {
      if (
        sportContent[index].style.height === "0px" ||
        sportContent[index].style.height === ""
      ) {
        sportIcon[index].style.transform = "rotate(0deg)";
        sportContent[index].style.marginTop = "20px";
        sportContent[index].style.height = sportContent[index].scrollHeight + "px";
      } else {
        sportIcon[index].style.transform = "rotate(-90deg)";
        sportContent[index].style.height = "0";
        sportContent[index].style.marginTop = "0";
      }
    });
  })(i);

}

function clearRequests() {
  $.each(xhrArray, function(index, xhr) {
      xhr.abort(); // Abort each XHR object
  });
  xhrArray = []; // Clear the array
}

$(document).ready(function () {
  $(".loader").hide()
  $(".betting-container").show()
});


function renderUpcoming(array){

console.log(array)
if(array){
pricestring=``;
analysedString=``

for(let i=0;i<array.length;i++){
















  if(array[i]['odds'][0]["price"]>array[i]['odds'][2]["price"])
  {
  pricestring=`<span style="color: #ff6363">${Math.round(array[i]["odds"][0]["price"] * Math.pow(10, 1)) / Math.pow(10, 1)}</span> :
               <span style="color: #63ff7c">${Math.round(array[i]["odds"][2]["price"] * Math.pow(10, 1)) / Math.pow(10, 1)}</span>`
  
  }
  
  else{
  pricestring=`<span style="color: #ff6363">${Math.round(array[i]["odds"][2]["price"] * Math.pow(10, 1)) / Math.pow(10, 1)}</span> :
               <span style="color: #63ff7c">${Math.round(array[i]["odds"][0]["price"] * Math.pow(10, 1)) / Math.pow(10, 1)}</span>`;
  }
  
if(array[i]["analysed"]){
analysedString=`<center>
                                    <span style="width:30px;height:10px;color:#63ff7c">Analysed</span>
                                  </center>`
}
else{
analysedString=`<span style="width:30px;height:10px;color:red">Not analysed</span>
                                  </center>`

}




if(array[i]["isLive"]){

  $(".betting-container").append(`   

  <div class="betting-Item">
  <center><span style="background-color:red;color:white; width:30px;height:10px">LIVE</span></center>
    ${analysedString}
  <div class="betting-team-box">
    <div class="betting-team" style="margin-right:50px">

    <img src="${array[i]['competitors'][0]['img']}" class="betting-team-image" />


      <p class="betting-team-name" style="font-size:14px">${array[i]['competitors'][0]["name"]}
      </p>
  </div>
  <center>
      <div class="betting-status-time-container">
      <center> <span class="first-team-score" style="margin-right:10px">${array[i]["score"][0]}</span>:<span class="second-team-score" style="margin-left:10px">${array[i]["score"][1]}</span></center>

        <div class="betting-status-container" style="padding-bottom:10px">

          ${pricestring}



        </div>
        <div class="betting-time-container">${array[i]['liveTime']}</div>

      </div>
    </center>
    <div class="betting-team" style="margin-left:50px">
      <img src="${array[i]['competitors'][1]['img']}" class="betting-team-image" />

      <p class="betting-team-name" style="font-size:14px">${array[i]["competitors"][1]["name"]}</p>
    </div>
  </div>
  <div class="betting-button-box" >
  <a class="betting-button" href="/analysis/${array[i]['id']}">
    Analysis
  </a>
</div>
</div>

`


);


}



else{
  $(".betting-container").append(`   

  <div class="betting-Item">
  <center><span class="betting-team-name"style="font-size:12px;">${array[i]['startDate']}</span></center>
${analysedString}
  <div class="betting-team-box">
    <div class="betting-team" style="margin-right:50px">

    <img src="${array[i]['competitors'][0]['img']}" class="betting-team-image" />


      <p class="betting-team-name" style="font-size:14px">${array[i]['competitors'][0]["name"]}</p>
  </div>
  <center>
      <div class="betting-status-time-container">

        <div class="betting-status-container" style="padding-bottom:10px">

          ${pricestring}



        </div>


      </div>
    </center>
    <div class="betting-team" style="margin-left:50px">
      <img src="${array[i]['competitors'][1]['img']}" class="betting-team-image" />

      <p class="betting-team-name" style="font-size:14px">${array[i]["competitors"][1]["name"]}</p>
    </div>
  </div>
  <div class="betting-button-box" >
  <a class="betting-button" href="/analysis/${array[i]['id']}">
    Analysis
  </a>
</div>
</div>

`


);
}








}
$(".loader").hide();
$(".betting-container").show();

}
else{

  $(".betting-container").append(`<Span style="  position: absolute;
  top: 50%;
  left: 55%;
  transform: translate(-50%, -55%);">There are no apropriate matches we could find.</Span>`)
}

}




const leagueDiv=document.getElementsByClassName("league")

let selectedleagues=[]

for(let i=0;i<leagueDiv.length;i++){

  (function(index) { // Create a closure to capture the current value of i
   

    $(leagueDiv[index]).on("click", function(){
      $(".sidebar").css("pointer-events","none")
      $(".loader").show();
      $(".betting-container").empty();
      $(".betting-container").hide();
      console.log(`clicked element of sportid ${leagueDiv[index].getAttribute("data-sportid")} and leagueid of ${leagueDiv[index].getAttribute("data-leagueid")}`)


      if($(leagueDiv[i]).hasClass("league-selected")){

        $(leagueDiv[i]).removeClass("league-selected");
        
        selectedleagues.splice(selectedleagues.indexOf(leagueDiv[i]),1);

      }
      else{

      $(leagueDiv[i]).addClass("league-selected");
      selectedleagues.push(
        {
          leagueid:leagueDiv[index].getAttribute("data-leagueid"),
          sportid:leagueDiv[index].getAttribute("data-sportid")
        }

  
        );

      }

      $.ajax({
        type: "POST",
        url: "/getUpcoming",
        data: JSON.stringify(selectedleagues),
        contentType: "application/json", 
        success: function(response) {
          
          renderUpcoming(response)
          
          $(".sidebar").css("pointer-events","auto")
        },
        error:function(response){
          $(".loader").hide();
          $(".sidebar").css("pointer-events","auto")
        }

      });



      console.log(selectedleagues)

    })


    

  })(i);



}













