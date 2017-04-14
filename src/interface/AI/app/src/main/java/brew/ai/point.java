package brew.ai;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

/**
 * Created by cody on 3/6/17.
 */

public class point {
    @SerializedName("temp")
    @Expose
    float temp;
    @SerializedName("co2")
    @Expose
    float co2;
    @SerializedName("grav")
    @Expose
    float grav;
    @SerializedName("time")
    @Expose
    float time;

    public static point parseJSON(String response) {
        Gson gson = new Gson();
        point p = gson.fromJson(response, point.class);
        return p;
    }
    public String toString(){
        String tmp;
        tmp = Float.toString(temp) + " " + Float.toString(co2) + " " + Float.toString(grav) + " " + Float.toString(time);
        return tmp;
    }
}
