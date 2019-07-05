# orangepi-ws2812
WAMP + WS2812B LEDs on the Orange Pi Zero


## Packages required:

- python3-smbus


## The I2C protocol

Command data:

| Command | Description                 |
|---------|-----------------------------|
| 0       | Blank to off                |
| 1       | Write pixel values          |
| 10      | Display pixel values        |

### Drawing pixel values (command: 1)

| Byte    | Purpose                 |
|---------|-------------------------|
|  0      | Number of bytes to follow |
|  1      | Pixel offset (0 offset) |
|  2      | Reserved                |
|  3      | Number of pixels        |
|  4      | R value for pixel 0     |
|  5      | R value for pixel 0     |
|  6      | R value for pixel 0     |
|  7      | R value for pixel 1     |
|  8      | R value for pixel 1     |
|  9      | R value for pixel 1     |
| 10      | R value for pixel 2     |
| 11      | R value for pixel 2     |
| 12      | R value for pixel 2     |
| 13      | R value for pixel 3     |
| 14      | R value for pixel 3     |
| 15      | R value for pixel 3     |
| 16      | R value for pixel 4     |
| 17      | R value for pixel 4     |
| 18      | R value for pixel 4     |
| 19      | R value for pixel 5     |
| 20      | R value for pixel 5     |
| 21      | R value for pixel 5     |
| 22      | R value for pixel 6     |
| 23      | R value for pixel 6     |
| 24      | R value for pixel 6     |
| 25      | R value for pixel 7     |
| 26      | R value for pixel 7     |
| 27      | R value for pixel 7     |
| 28      | R value for pixel 8     |
| 29      | R value for pixel 8     |






