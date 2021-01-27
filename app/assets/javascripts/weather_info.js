// Place all the behaviors and hooks related to the matching controller here.
// All this logic will automatically be available in application.js.


function to_datetime(str) {
    var year = str.substr(0, 4)
    var month = str.substr(4, 2)
    var day = str.substr(6, 2)
    var hour = str.substr(8, 2) + ":00:00"
    var daystr = year + "/" + month + "/" + day + " " + hour
    var date = new Date(daystr)
    return date
  }
  
  function controller_gen(gon_array) {
    return_array = []
    var n = 0;
    for (var i = 0, len = gon.sorted.length; i < len; ++i) {
      if (n == 0) {
        var r = 0;
      } else {
        var r = n - 1;
      }
      if (gon.sorted[i] === gon_array[n]) {
        n++
        r++
      }
      if (gon.sorted[i] === gon_array[0]) {
        return_array.push(gon_array[0])
      } else {
        return_array.push(gon_array[r]);
      }
  
    }
    return return_array
  }
  
  function find_index(time, kind) {
    kind_of_array = { time: gon.sorted, chart: gon.chart, wind: gon.wind, wave: gon.wave }
    gon_array = kind_of_array[kind]
    controller_array = controller_gen(gon_array)
    index = gon.sorted.indexOf(time)
    controller_array.indexOf(index)
    return Number(gon_array.findIndex(item => item == controller_array[index]))
  }
  
  // ここからjquery
  $(function () {
  
    $('#hour-0in0 a').addClass('active')
  

    //  作業中
    var id_memo = 0
    $('#' + id_memo + '.dr-time').removeClass('hide')
    $('.dr-day').on('change', function () {
      $('.carousel').off('slide.bs.carousel')
      var id = $(this).children(':selected').attr('id')
      $('#' + id_memo + '.dr-time').addClass('hide')
      $('#' + id + '.dr-time').removeClass('hide')
      console.log(id)
      id_memo = id
    })


    
    function carousel_controll(id, type = "") {
      console.log("carousel:" + id + "/" + type)
      if (type != "time") { $('#TimeImageControll').carousel(find_index(id, 'time')) }
      if (type != "chart") { $('#ChartImageControll').carousel(find_index(id, 'chart')) }
      if (type != "wind") { $('#WindImageControll').carousel(find_index(id, 'wind')) }
      if (type != "wave") { $('#WaveImageControll').carousel(find_index(id, 'wave')) }
    }
  
    function add_active_class(index) {
      $('.hours a').removeClass('active')
      i = '#hour-' + index + "in0 a"
      $(i).addClass('active')
      var id = $(i).attr('id')
      console.log(id)
      carousel_controll(id)
    }
  
    function nav_bar_controll(index) {
      //   date, hours a, 
      console.log("==================")
      var hourtab = $('.hours #' + index).parent().parent().parent()
      console.log(hourtab.attr('id'))
      $('.hours a').removeClass('active')
      $('.tab-pane').removeClass('show active')
      var i = hourtab.attr('id').substr(4, 1)
      console.log(i)
      $('.nav-tabs .nav-item').removeClass('active')
  
      $('.nav-tabs #' + i).addClass('active')
      $('.hours #' + index).addClass('active')
      hourtab.addClass('show active')
      console.log('-----------------')
    }
  
    $('.nav-click').on('click', function () {
      $('.carousel').off('slide.bs.carousel')
      var id = $(this).attr('id')
      add_active_class(id)
    })
  
    $('.click').on('click', function () {
      $('.carousel').off('slide.bs.carousel')
      var id = $(this).attr('id');
      carousel_controll(id)
    })
  
    $('.chart-button').on('click', function () {
      $('.carousel').off('slide.bs.carousel')
      $('.chart').on('slide.bs.carousel', function (e) {
        carousel_id = $(this).children('div').children('#' + e.to).attr('carousel-number')
        carousel_controll(carousel_id, 'chart')
        nav_bar_controll(carousel_id)
      })
    })
    $('.wind-button').on('click', function () {
      $('.carousel').off('slide.bs.carousel')
      $('.wind').on('slide.bs.carousel', function (e) {
        carousel_id = $(this).children('div').children('#' + e.to).attr('carousel-number')
        carousel_controll(carousel_id, 'wind')
        nav_bar_controll(carousel_id)
      })
    })
    $('.wave-button').on('click', function () {
      $('.carousel').off('slide.bs.carousel')
      $('.wave').on('slide.bs.carousel', function (e) {
        carousel_id = $(this).children('div').children('#' + e.to).attr('carousel-number')
        carousel_controll(carousel_id, 'wave')
        nav_bar_controll(carousel_id)
      })
    })
    $('#ChartImageControll').on('touchstart', function () {
      console.log('touchstart-chart')
      $('.carousel').off('slide.bs.carousel')
      $('.chart').on('slide.bs.carousel', function (e) {
        carousel_id = $(this).children('div').children('#' + e.to).attr('carousel-number')
        carousel_controll(carousel_id, 'chart')
        nav_bar_controll(carousel_id)
      })
    })
    $('#WindImageControll').on('touchstart', function () {
      console.log('touchstart-wind')
      $('.carousel').off('slide.bs.carousel')
      $('.wind').on('slide.bs.carousel', function (e) {
        carousel_id = $(this).children('div').children('#' + e.to).attr('carousel-number')
        carousel_controll(carousel_id, 'wind')
        nav_bar_controll(carousel_id)
      })
    })
    $('#WaveImageControll').on('touchstart', function () {
      console.log('wave')
      $('.carousel').off('slide.bs.carousel')
      $('.wave').on('slide.bs.carousel', function (e) {
        carousel_id = $(this).children('div').children('#' + e.to).attr('carousel-number')
        carousel_controll(carousel_id, 'wave')
        nav_bar_controll(carousel_id)
      })
    })
  })
  