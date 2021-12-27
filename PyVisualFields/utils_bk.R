# -*- coding: utf-8 -*-

# Created on Mon Oct 11 22:16:54 2021

# @author: Mohammad Eslami 
# Massachusetts Eye and Ear
# Harvard Medical School

# this file contains required utilities in R

library(visualFields)

# getgpar()$colmap$map$probs
# getgpar()$colmap$map$cols
# getgpar()$progcolmap$b$map$probs
# getgpar()$progcolmap$b$map$cols

drawcolscalesfa <- function(probs, cols, ...) {
  if(!(0 %in% probs)) {
    probs <- c(0, probs)
    cols  <- c("#000000", cols)
  }
  colrgb <- col2rgb(cols) / 255
  txtcol <- rep("#000000", length(probs))
  txtcol[(0.2126 * colrgb[1,]
          + 0.7152 * colrgb[2,]
          + 0.0722 * colrgb[3,]) < 0.4] <- "#FFFFFF"
  pol <- NULL
  y <- c(0.5, 0.5, -0.5, -0.5)
  xini <- (26 - length(probs)) / 2
  xend <- 25 - xini
  pol[1] <- list(data.frame(x = c(xini, xini + 1, xini + 1, xini), y = y))
  for(i in 2:length(probs)) {
    xl <- pol[[i-1]]$x[2]
    xu <- xl + 1
    pol[i] <- list(data.frame(x = c(xl, xu, xu, xl), y = y))
  }
  x <- xini + 1:length(probs)
  y <- rep(0, length(probs))
  defpar <- par(no.readonly = TRUE) # read default par
  on.exit(par(defpar))              # reset default par on exit, even if the code crashes
  par(mar = c(0, 0, 0, 0), ...)
  # dev.new(width=1, height=1)
  plot(x, y, typ = "n", ann = FALSE, axes = FALSE,
       xlim = c(1, 25), ylim = c(-0.25, 0.25), asp = 1)
  for(i in 1:length(x)) polygon(pol[[i]], border = NA, col = cols[i])
  text(x - diff(x)[1] / 2, y, probs, col = txtcol)
}

drawcolscalesfa(getgpar()$colmap$map$probs, getgpar()$colmap$map$cols, ps = 6)
