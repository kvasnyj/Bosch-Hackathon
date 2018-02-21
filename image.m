img = imread('/home/kvasnyj/repo/Bosch-Hackathon/img/1.jpg');

img = rgb2hsv(img);

[h, w] = size(img)

img = img(:,:,2);

x = [0, 0, w, w];
y = [h, h-500, h-500, h];
mask = roipoly(img, x , y);
img(mask==0) = 0;

img = edge(img, 'Canny', 0.2);  

imshow(img);

