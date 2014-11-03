function addLoadEvent(func) {//func是要加载的函数名
     var oldonload = window.onload;
      if(typeof window.onload != 'function' ) {
               window.onload = func;//如果是加载的第一个函数，就像普通的加载一样
     }else {
               window.onload = function() {//如果已经加载了函数，就把func也一起加载了
                    oldonload();
                    func();
               }
     }
}
