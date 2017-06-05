function init () {
  const width = document.querySelector('#frontpage').offsetWidth
  const height = width * 0.7
  const canvas = document.querySelector('#spiral')
  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext('2d', {})

  drawSpiral(ctx, 0, 0, width, height)
}

function drawSpiral (ctx, x, y, width, height) {
  const center = {
    x: x + width / 2.0,
    y: y + height / 2.0
  }

  const stepCount = 4096
  const DELTA = 0.5   // delta per round
  const exponent = 3.5
  const ROTATIONS = 10.0

  const Color = function (r, g, b) {
    this.r = r
    this.g = g
    this.b = b
    this.toString = function () { return 'rgb(' + this.r + ',' + this.g + ',' + this.b + ')' }
    this.scaleTo = function (color, t) {
      return new Color(Math.floor(this.r + (color.r - this.r) * t),
        Math.floor(this.g + (color.g - this.g) * t),
        Math.floor(this.b + (color.b - this.b) * t)
      )
    }
  }

  ctx.lineWidth = 3
  let startColor = new Color(0, 0, 0)
  let endColor = new Color(200, 200, 200)
  ctx.strokeStyle = startColor.toString()

  let theta = 0.0
  let delta = 0.0
  let oldPoint = { x: center.x, y: center.y }
  let point, t
  (function drawInvert () {
    (function drawStep (step) {
      setTimeout(() => {
        const nextStep = step + 50
        while (step < nextStep) {
          t = step / (stepCount - 1)
          point = { x: center.x + Math.cos(theta) * delta, y: center.y + Math.sin(theta) * delta }
          ctx.strokeStyle = startColor.scaleTo(endColor, t).toString()
          ctx.beginPath()
          ctx.moveTo(oldPoint.x, oldPoint.y)
          ctx.lineTo(point.x, point.y)
          ctx.stroke()
          theta -= ROTATIONS * (Math.PI * 2) / stepCount
          delta = Math.pow(step * (DELTA / (stepCount / ROTATIONS)), exponent)
          oldPoint.x = point.x
          oldPoint.y = point.y
          ++step
        }
        if (step < stepCount) {
          drawStep(++step)
        }
      }, 5)
    })(0)
    setTimeout(() => {
      const buf = startColor
      startColor = endColor
      endColor = buf
      drawInvert()
    }, (stepCount / 50) * 5)
  })()
}

document.addEventListener('DOMContentLoaded', init)
