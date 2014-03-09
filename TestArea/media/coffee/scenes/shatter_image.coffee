class point
  x:  0,  y: 0 #position
  vx: 0, vy: 0 #speed
  sx: 0, sy: 0 #start point
  glow: false #allow glow (very slow)
  spread: 1 #speed spread
  constructor: (@x, @y, @color) ->
    @sx = @x
    @sy = @y
    @spread = 1+Math.random()

  draw: (h) ->
    if @glow
      h.globalAlpha = 0.01
      h.beginPath()
      h.fillStyle = 'white';
      h.arc(@x, @y, 10, 0, Math.PI*2);
      h.fill()
      h.closePath()

    h.globalAlpha = 1
    h.beginPath()
    h.fillStyle = @color
    h.rect(@x, @y, 2, 2)
    h.fill()
    h.closePath()

  force_to_point: (magnitude, x, y, dt, dacceleration, minspeed) ->
    dx = x-@x
    dy = y-@y
    norm = Math.sqrt(dx*dx+dy*dy)
    if norm<100
      norm=100
    fx = magnitude*dx/norm
    fy = magnitude*dy/norm
    @force(fx, fy, dt, dacceleration, minspeed)
  force_back: (magnitude, dt, dacceleration, minspeed = 0) ->
    @force_to_point(magnitude, @sx, @sy, dt, dacceleration, minspeed)
  force: (fx, fy, dt, dacceleration, minspeed) ->
    @vx += fx*dt
    @vy += fy*dt
    if Math.abs(@vx)>minspeed or Math.abs(@vy)>minspeed
      @vx *= 1 / (1+dt*dacceleration)
      @vy *= 1 / (1+dt*dacceleration)
    else
      if Math.random()>.9
        alpha = Math.PI / 50
        vx2 = (@vx * Math.cos(alpha)) + (@vy*Math.sin(alpha))
        vy2 = (-@vx * Math.sin(alpha)) + (@vy*Math.cos(alpha))
        @vx = vx2
        @vy = vy2
    delta_x = @vx*@spread*dt
    delta_y = @vy*@spread*dt
    @x += delta_x
    @y += delta_y
    return Math.abs(delta_x) + Math.abs(delta_y)

class shatter_image
  constructor: (@image, @g, @canvas, @width_proportion, @height_proportion, @ai) ->
    width = $(@image).width()
    height = $(@image).height()
    image_x = $(@image).offset().left - $(@canvas).offset().left
    image_y = $(@image).offset().top - $(@canvas).offset().top
    @points = []
    @mean = 2
    @toPoint = true
    @age = 0

    @g.clearRect(0, 0, width, height)
    @g.drawImage(@image, 0, 0, width, height)
    try
      @ai.stop.apply(@ai)
    $(@image).hide()
    @data = @g.getImageData(0, 0, width, height)

    size = @data.height * @data.width / 4
    if size > 20000
      @mean = 4
    if size > 50000
      @mean = 8

    for j in [0...@data.height] by @mean
      for i in [0...@data.width] by @mean
        average = 0
        a_r = 0; a_g = 0; a_b = 0; a_a = 0

        for y in [j...j+@mean]
          for x in [i...i+@mean]
            index = 4*(j*@data.width+i)
            r = @data.data[index]
            g = @data.data[index+1]
            b = @data.data[index+2]
            a = @data.data[index+3]
            a_r += r; a_b += b; a_g += g; a_a += a
            average += (r+g+b) / 3 * (a / 255)
        average = average/(@mean*@mean)

        if average>0
          #console.log average
          a_r = a_r/(@mean*@mean); a_g = a_g/(@mean*@mean); a_b = a_b/(@mean*@mean); a_a = a_a/(@mean*@mean)
          color = "rgba("+a_r+","+a_g+","+a_b+","+a_a / 255+")"
          p = new point((i + image_x) / @width_proportion,(j + image_y) / @height_proportion, color)
          @points.push p

  restore: ->
    $(@image).show()
    try
        @ai.start.apply(@ai)

class swarm_creator
  #toPoint: false
  time:  50
  speed: 50
  force: 0.00001
  dacceleration: 0.001
  minspeed: 0.005
  x: 100
  y: 100
  images: []
  constructor: (@canvas, @width, @height, @hidden, @width_proportion, @height_proportion) ->
    setInterval =>
      @calc()
      @clear()
      @draw()
    ,@time
  calc: ->    
    list = @images
    @images = []
    for image in list
      image.age++
      sum = 0
      for p in image.points
        if image.toPoint
          sum += p.force_to_point(@force/10, @x, @y, @speed*@time, @dacceleration, @minspeed)
        else
          sum += p.force_back(@force, @speed*@time, @dacceleration)
      if sum > 30
        @images.push image
      else
        image.restore()
  draw: ->
    for image in @images
      for p in image.points
        #p.glow = @toPoint
        p.draw(@canvas)
  clear: ->
    @canvas.clearRect(0, 0, @width, @height)
  add: (img, ai) ->
    sh = new shatter_image(img, @canvas, @hidden, @width_proportion, @height_proportion, ai)
    @images.push(sh)
  restore: ->
    for image in @images
      if image.age>10
        image.toPoint = false

class swarm_ui
  constructor: ->
    @canvas = $('.canvas-sketch')
    @hidden = $('.canvas-release')
    @width = @hidden.width()
    @height = @hidden.height()
    @g = @canvas[0].getContext('2d')
    @h = @hidden[0].getContext('2d')
    @width_proportion = @width/@hidden.attr('width')
    @height_proportion = @height/@hidden.attr('height')
    swarm = new swarm_creator(@h, @width, @height, @hidden, @width_proportion, @height_proportion)
    $('html').click (e)->      
      swarm.restore()
    $('html').mousemove (e) =>
      swarm.x = (e.pageX - $(@hidden).offset().left) / @width_proportion
      swarm.y = (e.pageY - $(@hidden).offset().top) / @height_proportion
      if swarm.x<10 or swarm.x>@hidden.attr('width') - 10 or swarm.y<10 or swarm.y>@hidden.attr('height') - 10
        swarm.x = 100
        swarm.y = 100
    $('img').click (e) =>
      swarm.restore()
      e.preventDefault()
      swarm.add(e.target, e.target.ai)

new swarm_ui
