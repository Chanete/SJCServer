# SJCServer Package
Este paquete esta diseñado para realizar las transmisiones via YouTube de la parroquia San Juan Crisostomo de Madrid. 
Se puede reutilizar para cualqueir otro tipo de retransmision ajustando los parametros en los ficheros de configuracion. Ver seccion *Parametros de Configuración*
Crearemos un usuario sjc para no estar siempre tirando del usuario root que no es muy bueno...
Es importante añadir este usuario a los que tienen autorizado el comando sudo para que esta guia funcione. 
Esto se consigue asi
    su -   (pide la clave del usuario root que disteis en la instalación)
    visudo 

Se abre la edicion del fichero sudoers buscar la seccion donde pone 

    # User privilege specification
    root    ALL=(ALL:ALL) ALL

y, añadid detras

    sjc     ALL=(ALL:ALL) ALL

pulsar Crtl-X , la tecla 'S' y Enter


##INSTALACIÓN
Partimos de un Debian (en este momento la 10.8). Durante la instalación hemos seleccionado que se instale el entorno gráfico LXDE. 

Lo primero que tenemos que hacer es actualizar el sistema con las últimas versiones (profilaxis...)
Esto lo hacemos con
    sudo apt update
    sudo apt upgrade
    sudo apt dist-upgrade

y reiniciamos
    sudo reboot

###Instalar paquetes necesario
Cuando arranque, lo siguiente que vamos a hacer es instalar todos los paquetes que necesitamos para que esto funcione: 
  
    sudo apt install nginx-full mosquitto mosquitto-clients obs-studio  vlc net-tools adb git -y 

###Instalar OBS-WebSockets

Para instalar este componente necesitamos ejecutar estos comandos:

    cd
    sudo apt-get install libboost-all-dev -y
    git clone --recursive https://github.com/Palakis/obs-websocket.git
    cd obs-websocket
    mkdir build && cd build
    cmake -DLIBOBS_INCLUDE_DIR="<path to the libobs sub-folder in obs-studio's source code>" -DCMAKE_INSTALL_PREFIX=/usr -DUSE_UBUNTU_FIX=true ..
    make -j4
    sudo make install

###Instalar la aplicacion 

    cd 
    git clone

[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content. 