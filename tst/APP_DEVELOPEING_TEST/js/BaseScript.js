
var VERSION = "1.1.02";


var EMITIR;
var BAS_URL = "/SJC/";
var titulo_inic;
var titulo;
var SELECTOR;
var Estilo1 = "background-color: #98FF0B;cursor:pointer";
var Estilo2 = "background-color: #0BFFE7;cursor:pointer";
var est1 = "background-color: #00ACFF;cursor:pointer";
var est2 = "background-color: #44FF00;cursor:pointer";
var est;
var Selected_Emit;




function Version(){
  document.getElementById("DSP_VERSION").innerHTML+=VERSION;
}

function C_Altar(){
  fetch('http://sjc.itelsys.com:1313/SJC/MovetoPreset?plano=Altar');
    document.getElementById('Disp_source').src="sources/Altar.jpeg";
}
function C_General(){
  fetch('http://sjc.itelsys.com:1313/SJC/MovetoPreset?plano=General');
    document.getElementById('Disp_source').src="sources/Plano_General.jpeg";
  }
  function C_Virgen(){
    fetch('http://sjc.itelsys.com:1313/SJC/MovetoPreset?plano=Virgen');
      document.getElementById('Disp_source').src="sources/Virgen.jpeg";
  }

  function C_Nino(){
    fetch('http://sjc.itelsys.com:1313/SJC/MovetoPreset?plano=Ninio');
      document.getElementById('Disp_source').src="sources/Ninio.jpeg";
  }
  function C_Comunion(){
    fetch('http://sjc.itelsys.com:1313/SJC/MovetoPreset?plano=Comunion');
      document.getElementById('Disp_source').src="sources/Comunion.jpeg";
  }


function openNav() {
  document.getElementById("mySidenav").style.width = "100%";
}

/* Close/hide the sidenav */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}



function Cambio(Difer){
  if(Difer == 1){
    //  var estilo =   document.getElementById('screen_1').style;
    document.getElementById('screen_1').style="display:none";
    document.getElementById('screen_2').style="display:true";
  }
  else if(Difer == 2){

    document.getElementById('screen_1').style="display:none";
    document.getElementById('screen_4').style="display:true";

    Emitir_Directo();
  }
  else if(Difer == 3){
    document.getElementById('screen_2').style="display:none";
    document.getElementById('screen_3').style="display:true";
    document.getElementById('RESPUESTA').innerHTML ="";
    Fecha();
    EMITIR = "Interno";
    document.getElementById('EMITIR').innerHTML ="Emitir en: " + EMITIR;
    titulo_inic = document.getElementById('titulo').value;
    titulo = titulo_inic;
    auto="True";
    document.getElementById('img_auto').source="sources/tick.png";
  }
  else if(Difer == 4){
    document.getElementById('screen_2').style="display:none";
    document.getElementById('screen_3').style="display:true";
    document.getElementById('RESPUESTA').innerHTML ="";
    Fecha();
    EMITIR = "SJC";
    document.getElementById('EMITIR').innerHTML ="Emitir en: " + EMITIR;
    titulo_inic = document.getElementById('titulo').value;
    titulo = titulo_inic;
  }
  else   if(Difer == 6){
      //  var estilo =   document.getElementById('screen_1').style;
      document.getElementById('screen_1').style="display:none";
      document.getElementById('screen_6').style="display:true";
      Estado();
    }
  document.getElementById('BACK').style="background-color:#FF8C0B;display:true";
}





function Menu(){
  document.getElementById('screen_1').style="display:none";
  document.getElementById('screen_2').style="display:none";
  document.getElementById('screen_3').style="display:none";
  document.getElementById('screen_4').style="display:none";
  document.getElementById('screen_5').style="display:none";
  document.getElementById('screen_6').style="display:none";
  document.getElementById('screen_1').style="display:true";
  document.getElementById('BACK').style="background-color:#FF8C0B;display:none";



    document.getElementById('MainFrame').innerHTML = ' <div class="col-12">  <div  align="center">    <p id = "Status_Display"></p>  </div></div><div class="col-4" style="display:none" id="CABECERA1">  <div  align="left">    <p>Titulo:</p>  </div></div><div class="col-4" style="display:none" id="CABECERA2">  <div  align="left"  >    <p>Fecha:</p>  </div></div><div class="col-3" style="display:none" id="CABECERA3">  <div  align="left" >    <p>Canal:</p>  </div></div><div class="col-1" style="display:none" id="CABECERA4">  <div  align="left" >    <p>Estado:</p>  </div></div> ';
}








function Fecha(){
  var date = new Date();
  var min_date = date.toISOString().slice(0,10);
  var h=date.getHours();
  var m=date.getMinutes();

  m=m+6;
  if (m>59)
  {
    m=m-59;
    h=h+1;
  }

  if (h>23)
    h=h-23; 

  if (h<10)
    h="0"+h; 
  if (m<10)
    m="0"+m;
  var min_time = h+":"+m; 
  
  document.getElementById('Fecha').value =min_date;
  document.getElementById('hora').value =min_time;
}




var auto="True";
function automatico(){
  if(auto == "True"){
    auto = "False";
    document.getElementById('img_auto').src="sources/x.png";
    }
  else
  {
    auto = "True";
    document.getElementById('img_auto').src="sources/tick.png";
  }

}

function Programar(){
  document.getElementById('RESPUESTA').innerHTML = "<br> Cargando...";
  titulo= document.getElementById('titulo').value;
if(titulo_inic == titulo){

  fetch('/SJC/Programa_Misa?fecha='+ document.getElementById('Fecha').value +"%20"+ document.getElementById('hora').value +"&canal="+EMITIR+"&AUTO="+auto)
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {
      if(respuesta.msg == "ok"){
    document.getElementById('RESPUESTA').innerHTML = "Directo con titulo:"+ respuesta.titulo +" programado a las: "+ respuesta.publicado_el;
  }
  else {
      document.getElementById('RESPUESTA').innerHTML ="ERROR: "+respuesta.msg;
  }
})
}

else{

  fetch('/SJC/Programa_Misa?fecha='+ document.getElementById('Fecha').value +"%20"+ document.getElementById('hora').value +"&canal="+EMITIR  + "&titulo=" +encodeURI(titulo)+"&AUTO="+auto)
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {

    if(respuesta.msg == "ok"){
  document.getElementById('RESPUESTA').innerHTML = "Directo con titulo: "+ respuesta.titulo +" programado a las: "+ respuesta.publicado_el ;
}
else {
    document.getElementById('RESPUESTA').innerHTML ="Error: "+respuesta.msg;
}

    })
  titulo_inic ="";
  titulo = "";
  document.getElementById('titulo').value=" ";

}

}



function Emitir_Directo(){

  document.getElementById('Status_Display').innerHTML = "Porfavor espere.<br>Cargando...";
  fetch('/SJC/GetTransmissions?')
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {

    document.getElementById('Status_Display').innerHTML = "";
    document.getElementById('CABECERA1').style = "display:true; background-color: #A6A6A6";
    document.getElementById('CABECERA2').style = "display:true; background-color: #A6A6A6";
    document.getElementById('CABECERA3').style = "display:true; background-color: #A6A6A6";
    document.getElementById('CABECERA4').style = "display:true; background-color: #A6A6A6";
    SELECTOR =  respuesta.items;
  for(item in SELECTOR){
    if ( item % 2){
      Estilo = Estilo1;
    }
    else{
      Estilo = Estilo2;
    }
      r= SELECTOR[item];
      if(r["status"]=="live"){
        Emision(item);
      }
      document.getElementById('MainFrame').innerHTML =  document.getElementById('MainFrame').innerHTML + ' <div  class="col-3"  onclick="Emision(' + item + ')"  style ="'+ Estilo +'" >  <div  align="left"> <p class = "Lista" id="titulo=' + item + '" ></p>  </div>  </div>';
      document.getElementById("titulo="+item).innerHTML = r["titulo"];
      document.getElementById('MainFrame').innerHTML =  document.getElementById('MainFrame').innerHTML + ' <div  class="col-5"  onclick="Emision(' + item + ')" style ="'+ Estilo +'" >  <div  align="left" > <p class = "Lista" id="fecha=' + item + '" ></p>  </div>  </div>';
      document.getElementById("fecha="+item).innerHTML = r["Fecha_Sched"];
      document.getElementById('MainFrame').innerHTML =  document.getElementById('MainFrame').innerHTML + ' <div  class="col-2"  onclick="Emision(' + item + ')" style ="'+ Estilo +'" >  <div  align="left" > <p class = "Lista" id="canal=' + item + '" ></p>  </div>  </div>';
      document.getElementById("canal="+item).innerHTML = r["Canal"];
      document.getElementById('MainFrame').innerHTML =  document.getElementById('MainFrame').innerHTML + ' <div  class="col-2"  onclick="Borrar(' + item + ')" style ="'+ Estilo +'" >  <div  align="left" ><img src="sources/eliminar.png" style="width:100%;length:100%;margin:15px 0px 15px 0px;" </div>  </div>';

              };
  })
}
function Borrar(Emit){
    fetch('http://sjc.itelsys.com:1313/SJC/DeleteBroadcast?bid='+SELECTOR[Emit]["broadcast_id"]+'&canal='+SELECTOR[Emit]["Canal"]).then((respuesta)=>{
      return respuesta.json();
    }).then((respuesta) => {

      document.getElementById('Delete_Emision').innerHTML =respuesta.msg;

      })
      Menu();
}


function Emision(emit){
  Selected_Emit = emit;
  var id = SELECTOR[emit]["streamId"];
  var canal = SELECTOR[emit]["Canal"];
  document.getElementById('screen_4').style="display:none";
  document.getElementById('screen_5').style="display:true";


  if (SELECTOR[Selected_Emit]["status"] == "live"){
    document.getElementById('Start_Emision').innerHTML ="EN DIRECTO";
    document.getElementById('Start_Emision').style = "background-color: #28FF00";
    document.getElementById('dir').innerHTML='<iframe  width="560" height="315"src="https://youtube.com/embed/'+ SELECTOR[Selected_Emit]["broadcast_id"] +'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
    openNav();
    C_General();
  }
  else {
    document.getElementById('Start_Emision').innerHTML ="EMITIR";
    document.getElementById('Start_Emision').style = "background-color:#337BFF";
  }
}





function EmpezarEmision(){
    openNav();
    C_General();

    document.getElementById("Start_Emision").innerHTML = "Cargando...";

    document.getElementById('Start_Emision').style = "background-color: ##337BFF";

    fetch('/SJC/StartStreaming?sid='+SELECTOR[Selected_Emit]["streamId"]+"&canal=" +SELECTOR[Selected_Emit]["Canal"]+"&bid=" +SELECTOR[Selected_Emit]["broadcast_id"] )
    .then((respuesta)=>{
      return respuesta.json();
    }).then((respuesta) => {
      if(respuesta.msg == "Ok"){
            document.getElementById('Start_Emision').innerHTML ="EN DIRECTO";
            document.getElementById('Start_Emision').style = "background-color: #28FF00";

      }
      else{
              document.getElementById('Start_Emision').innerHTML ="ERROR<br>No se ha podido comenzar la emision : <br>" + respuesta.msg;

              document.getElementById('Start_Emision').style = "background-color: #FF4900";
          }
    })


//    document.getElementById('dir').innerHTML='<iframe  width="560" height="315"src="https://youtube.com/embed/'+ SELECTOR[Selected_Emit]["broadcast_id"] +'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';


}

function Parar(){

      document.getElementById("Stop_Emision").innerHTML = "Cargando...";
      document.getElementById('Stop_Emision').style = "background-color: ##FF4900";

  fetch('/SJC/StopStreaming?canal=' +SELECTOR[Selected_Emit]["Canal"]+"&bid=" +SELECTOR[Selected_Emit]["broadcast_id"] )
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {
    if(respuesta.msg == "Ok"){
        Menu();
    }
    else{
            document.getElementById('Stop_Emision').innerHTML ="ERROR<br>No se ha podido detener la emision : <br>" + respuesta.msg;

            document.getElementById('Stop_Emision').style = "background-color: #FF4900";
        }
  })

}


function Proyectar(){
document.getElementById("Proyectar").style="background-color:#2FEE07;cursor:pointer";
  fetch('/SJC/StartFireTV?bid='+SELECTOR[Selected_Emit]["broadcast_id"] );
}


function Estado(){

document.getElementById("EST_SALA").innerHTML="Comprobando estado de sala...";

}


function EncenderS(){
  fetch('/SJC/Sala?Estado=ON')
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {


  })
}

function ApagarS(){
  fetch('/SJC/Sala?Estado=OFF')
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {


  })
}


function EncenderP(){
  fetch('/SJC/Proyector?Estado=ON')
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {



  })
}

function ApagarP(){
  fetch('/SJC/Proyector?Estado=OFF')
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {



  })
}

function EncenderSon(){
  fetch('/SJC/Audio?Estado=ON')
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {



  })
}

function ApagarSon(){
  fetch('/SJC/Audio?Estado=OFF')
  .then((respuesta)=>{
    return respuesta.json();
  }).then((respuesta) => {



  })
}
