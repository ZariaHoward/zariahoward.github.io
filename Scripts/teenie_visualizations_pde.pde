JSONObject json;

void setup() {

  json = loadJSONObject("/Users/zariahoward/Documents/3448_Export.json");

  JSONArray faceHorizontalPercentile = json.getJSONArray("faceHorizontalPercentile");
  JSONArray faceVerticalPercentile = json.getJSONArray("faceVerticalPercentile");
  JSONArray regressionLineSlopes = json.getJSONArray("regressionLineSlopes");
  JSONArray regressionLineIntercepts = json.getJSONArray("regressionLineIntercepts");
  JSONArray hoffLineRhos = json.getJSONArray("hoffLineRhos");
  JSONArray hoffLineThetas = json.getJSONArray("hoffLineThetas");
  JSONArray numFaces = json.getJSONArray("numFaces");
  JSONObject individuals = json.getJSONObject("individuals");
  
  //for (int i = 0; i < values.size(); i++) {
    
  //  JSONObject animal = values.getJSONObject(i); 

  //  int id = animal.getInt("id");
  //  String species = animal.getString("species");
  //  String name = animal.getString("name");

  //  println(id + ", " + species + ", " + name);
  //}

//Vertical Percentile Display
//PImage Zar = loadImage("/Users/zariahoward/Documents/TH_Tester/Box_022/3318.png"); //1600 x 1265
//float[] Percentiles = new float [faceHorizontalPercentile.size()];
//for (int i = 0; i < Percentiles.length; ++i) {
//   Percentiles[i] = faceHorizontalPercentile.getFloat(i); //Percentiles of the vertical lines
//}
//size(800,632);
//image(Zar,0,0,800,632);
//for (int i = 0; i < Percentiles.length; ++i) {
//  stroke(255,0,100,15);
//  strokeWeight(5);
//  int xValue = int(Percentiles[i]*800);
//  println(xValue);
//  line(xValue,0,xValue,632);
//}


//Horizontal Percentile Display

//PImage Zar = loadImage("/Users/zariahoward/Documents/TH_Tester/Box_022/3345.png"); //1600 x 1282
//float[] Percentiles = new float [faceVerticalPercentile.size()];
//for (int i = 0; i < Percentiles.length; ++i) {
//   Percentiles[i] = faceVerticalPercentile.getFloat(i); //Percentiles of the vertical lines
//}
//size(800,632);
//image(Zar,0,0,800,632);
//for (int i = 0; i < Percentiles.length; ++i) {
//  stroke(255,100,0,10);
//  strokeWeight(5);
//  int yValue = int(Percentiles[i]*632);
//  println(yValue);
//  line(0,yValue,800,yValue);
//}

//// Create an int array to accomodate the numbers.
//int[] numbers = new int[numFaces.size()];

//// Extract numbers from JSON array.
//for (int i = 0; i < numFaces.size(); ++i) {
//   numbers[i] = numFaces.getInt(i);
//}
//    //Number of Faces Display
  
//  PImage Zar = loadImage("/Users/zariahoward/Documents/TH_Tester/Box_008/2086.png"); //Choose image to overlay
//  image(Zar,0,0, 800, 640);
//  size(800, 640);
    
//  int maxFaces= max(numbers);
//  int[] histFaces = new int[maxFaces + 1];
//  for (int i = 0; i < numFaces.size(); i++) {
//    int a = numbers[i];
//    histFaces[a]+=1;
//  } 
  
//  println(histFaces);
  
//  // Find the largest value in the histogram
//  int histMax = max(histFaces);
//  int rectWidth = (Zar.width/2)/(maxFaces+1);
//  float verticalUnit = 0.442; //Zar.height/histMax;
//  print("VerticalUnit: ", verticalUnit);
//  stroke(255);
//  fill(76,0,153,120);
//  // Draw half of the histogram (skip every second value)
//  for (int i = 0; i <= maxFaces; i += 1) {
//    //(x,y,width,height)
//    stroke(255);
//    fill(76,0,153,120);
//    rect(i*rectWidth, (Zar.height/2)-int((verticalUnit*histFaces[i])), rectWidth,int((verticalUnit*histFaces[i])));
//    println(i);
//    println(i*rectWidth, (Zar.height/2)-int((verticalUnit*histFaces[i])), rectWidth,int((verticalUnit*histFaces[i])));
//    textSize(20);
//    textAlign(LEFT, BOTTOM);
//    fill(255);
//    text(str(histFaces[i]), i*rectWidth, (Zar.height/2)-int((verticalUnit*histFaces[i]))); 
//  }
//  textSize(25);
//  textAlign(CENTER,TOP);
//  text("Number of Faces in a Teenie Harris Photo", 400,0);
//  //

}