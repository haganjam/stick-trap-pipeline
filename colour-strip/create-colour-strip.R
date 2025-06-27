
library(ggplot2)

# Define colors and labels
colors <- c("red", "green", "blue", "cyan", "magenta", "yellow", "gray", "white", "black")
df <- data.frame(
  x = seq_along(colors),
  color = colors
)

# Plot
p <- ggplot(df, aes(x = factor(x), y = 1, fill = color)) +
  geom_tile(color = "black", linewidth = 2) +
  scale_fill_identity() +
  theme_void() +
  theme(legend.position = "none") +
  coord_fixed(ratio = 1)

p

# Save to file
ggsave("colour-strip/colour-strip.png", p, width = 9, height = 1.5, dpi = 1000)
