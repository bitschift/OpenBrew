package brew.ai;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.List;

/**
 * Created by cody on 3/6/17.
 */

public class point {
    float temp;
    float co2;
    float grav;
    int time;

    public static point parseJSON(String response) {
        Gson gson = new GsonBuilder().create();
        point p = gson.fromJson(response, point.class);
        return p;
    }
}
