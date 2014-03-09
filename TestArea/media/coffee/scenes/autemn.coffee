$C = @

class Autemn extends $C.Scene
  cell: new $C.Cell(0,1)
  container: $('.scene-autemn')

  ############################# Locations ###############################################################

  AsProgram: new $C.Location(-1000,-600)
  Portfolio: new $C.Location(1000,0)
  About: new $C.Location(0,700)

  enter: ->
    @cell.goto(@AsProgram)
    @mouseMove()

  ############################# Mouse move ##############################################################

  mouseMove: ->
    @container.mousemove((e)->
      alpha = 0.01
      x = e.pageX - $(@).offset().left
      y = e.pageY - $(@).offset().top
      $('.background-moving').css('left', -x*alpha)
      $('.background-moving').css('top', -y*alpha)
    )

  ############################# Clouds ##################################################################
  runCloud: (cloud, time, offset)->
    _cloud = @;
    cloud.animate
      left: "-300px"
      time
      'linear'
      ->
        $(@).css('left', $C.Screen.cell_width)
        setTimeout( ->
          speed = 500+$C.random(1000)
          length = $C.Screen.cell_width + offset + 300
          time = Math.floor(10000*length/speed)
          _cloud.runCloud(cloud, time, offset)
        )
        1000

  generateCloud: (holder)->
    cloudNumber = $C.random(28)
    id = 'cloud' + $C.random(1000) + "_" + $C.random(1000) + "_" + $C.random(1000)
    cloudDiv = "<img class='cloud' id='" + id + "' src='/media/images/clouds/" + cloudNumber + ".png' />"
    x = $C.random($C.Screen.cell_width)
    y = $C.random($C.Screen.cell_height)
    holder.append(cloudDiv)
    cloud = $('#' + id)
    cloud.css('left', x)
    cloud.css('top', y)
    speed = 500 + $C.random(1000)
    length = x + 300
    time = Math.floor(10000*length/speed)
    this.runCloud(cloud, time, 0)

  generateClouds: ->
    holder = $('.clouds', @container)
    for i in [1...10]
      @generateCloud(holder)
  ########################################################################################################


  constructor: ->
    @initialize()
    @generateClouds()

$C.Autemn = new Autemn
