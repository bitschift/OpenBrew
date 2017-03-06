package brew.ai;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by cody on 3/6/17.
 */

public class batch {
    //String name;
    List<point> points;

    public batch(){
        points = new ArrayList<point>();
    }
}
