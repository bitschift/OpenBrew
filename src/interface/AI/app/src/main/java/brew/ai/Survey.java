package brew.ai;

import android.app.Dialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.text.Layout;
import android.util.Log;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

public class Survey extends AppCompatActivity {
    // Smell: chemical, musty Taste: musty
    //            0       1            2
    int survey_values[]={0,0,0};
    LinearLayout main;
    int value;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_survey);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        main = (LinearLayout) findViewById(R.id.surveyContent);
        value = 0;

    }

    void submit(View v){
        ArrayList<CenterSeekBar> bars = new ArrayList<CenterSeekBar>();
        int ids[]={R.id.alcoholsmellbar, R.id.alcoholtastebar,R.id.appetizingbar,R.id.claritybar,R.id.honeysmellbar,R.id.sweetnessbar};
        Log.d("SURVEY:","Children:"+String.valueOf(main.getChildCount()));
        for(int i = 0;i < 6; i++){
            bars.add((CenterSeekBar) findViewById(ids[i]));
            Log.d("SURVEY:", "Logged CenterSeekBar at" + String.valueOf(i));
        }
        for(int i = 0; i < bars.size(); i++){
            value += (bars.get(i).getProgress()-50)/10;
            Log.d("SURVEY:", "Current value: "+String.valueOf(value));
        }
        for(int i = 0; i < 3; i++){
            value += survey_values[i];
        }
        Intent intent = new Intent();
        intent.putExtra("survey", String.valueOf(value));
        setResult(RESULT_OK, intent);
        finish();
    }

    void warning(View v){
        final Dialog dialog = new Dialog(this); // Context, this, etc.
        dialog.setContentView(R.layout.dialogue_warning);
        dialog.setTitle(R.string.app_name);
        dialog.show();
        switch(v.getId()){
            case R.id.chemicalyes:
                survey_values[0] = -10;
                break;
            case R.id.mustysmellyes:
                survey_values[1] = -10;
                break;
            case R.id.mustytasteyes:
                survey_values[2] = -10;
                break;
        }
    }
    void safe(View v){
        switch(v.getId()){
            case R.id.chemicalno:
                survey_values[0] = 0;
                break;
            case R.id.mustysmellno:
                survey_values[1] = 0;
                break;
            case R.id.mustytasteno:
                survey_values[2] = 0;
                break;
        }
    }

}
