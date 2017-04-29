package brew.ai;



import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Point;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.EditText;
import android.widget.Button;
import android.widget.Toast;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.LegendRenderer;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Set;
import java.util.UUID;

public class Main extends Activity
{
    //TextView myLabel;
    //TextView Label;
    //EditText myTextbox;
    BluetoothAdapter mBluetoothAdapter;
    BluetoothSocket mmSocket;
    BluetoothDevice mmDevice;
    OutputStream mmOutputStream;
    InputStream mmInputStream;
    Thread workerThread;
    volatile boolean stopWorker;
    batch results;
    int state = 0; // 0 is normal, 1 is pre-brew, 2 is brewing, 3 is post brew
    Integer dataBegin = 0;



    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button closeButton = (Button)findViewById(R.id.close);
        results = new batch();



        //Close button
        closeButton.setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View v)
            {
                try
                {
                    closeBT();
                }
                catch (IOException ex) { }
            }
        });
    }


    void launch(View v){
        Intent intent;
        switch(v.getId()){
            case R.id.button2:
                intent = new Intent(this, Survey.class);
                intent.putExtra("com.example.brew.ai.MESSAGE", "Are you kitten me?");
                startActivityForResult(intent, 1);
                break;
        }
    }

    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 1) {
            if(resultCode == RESULT_OK) {
                String survey = data.getStringExtra("survey");
                try {
                    sendData("{\"survey\":" + survey + "}");
                }
                catch(IOException e){

                }
            }
            final GraphView g[] = {(GraphView) findViewById(R.id.graph1),(GraphView) findViewById(R.id.graph2),(GraphView) findViewById(R.id.graph3)};
            for (GraphView graph:g) {
                graph.removeAllSeries();
            }
            results.points.clear();
        }
        if(requestCode == 2){
            try {
                sendData("start");
                state = 2;
            }
            catch(IOException e){}
        }

    }

    void openButt(View v){
        try
        {
            findBT();
            openBT();
        }
        catch (IOException ex) { }
    }

    void dataReq(View v){
        try {
            sendData("dataReq");
        }
        catch(IOException e){}
    }
    void start(View v){
        Intent intent = new Intent(this, BrewSetup.class);
        intent.putExtra("com.example.brew.ai.MESSAGE", "Are you kitten me?");
        startActivityForResult(intent,2);

    }

    void findBT()
    {
        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if(mBluetoothAdapter == null)
        {
            //myLabel.setText("No bluetooth adapter available");
            return;
        }

        if(!mBluetoothAdapter.isEnabled())
        {
            Intent enableBluetooth = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBluetooth, 0);
        }

        mBluetoothAdapter.setName("BrewAIUI");
        Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
        if(pairedDevices.size() > 0)
        {
            //Label.setText("Devices Found");
            for(BluetoothDevice device : pairedDevices)
            {
                //Label.append(device.getName());
                //if(device.getName().equals("cody-Lenovo-B590"))
                //{
                    mmDevice = device;
                    //myLabel.setText("Bluetooth Device Found");
                    break;
                //}
            }
        }
    }

    void openBT() throws IOException {
        if (mmDevice != null) {
            UUID uuid = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee"); //Standard SerialPortService ID
            mmSocket = mmDevice.createRfcommSocketToServiceRecord(uuid);
            mmSocket.connect();
            mmOutputStream = mmSocket.getOutputStream();
            mmInputStream = mmSocket.getInputStream();

            beginListenForData();

            //myLabel.setText("Bluetooth Opened");
        }
    }

    String parseBytes(InputStream mmInputStream){
        String recvdata = "";
        try {
            int bytesAvailable = mmInputStream.available();
            byte[] bytes = new byte[bytesAvailable];
            mmInputStream.read(bytes);
            int i;
            for (i = 0; i < bytesAvailable; i++) {
                if (bytes[i] == (byte) 10) //10 is a newline
                    break;
            }

            recvdata = new String(Arrays.copyOfRange(bytes, 0, i), "US-ASCII");
        }
        catch(IOException e){}
        return recvdata;
    }

    String getName(int i){
        if(i == 0){
            return getResources().getString(R.string.temp);
        }
        else if(i == 1){
            return getResources().getString(R.string.grav);
        }
        return getResources().getString(R.string.co2);
    }

    LineGraphSeries<DataPoint> getDataPoints(batch b, String str){
        DataPoint[] data = new DataPoint[b.points.size()];

        for(int j = 0; j < b.points.size(); j++){
            if(str.equals(getResources().getString(R.string.grav))){
                data[j] = new DataPoint(b.points.get(j).time, b.points.get(j).grav);
            }
            else if(str.equals(getResources().getString(R.string.co2))){
                data[j] = new DataPoint(b.points.get(j).time, b.points.get(j).co2);
            }
            else if(str.equals(getResources().getString(R.string.temp))){
                data[j] = new DataPoint(b.points.get(j).time, b.points.get(j).temp);
            }
        }

        return new LineGraphSeries<>(data);
    }
    void graph(GraphView g, batch b, String var){
        float high = 0;

        g.getViewport().setMinX(b.points.get(0).time-1);
        g.getViewport().setMaxX(b.points.get(b.points.size()-1).time+1);
        g.getViewport().setMinY(0);
        g.getViewport().setYAxisBoundsManual(true);
        g.getViewport().setXAxisBoundsManual(true);

        LineGraphSeries<DataPoint> data = getDataPoints(b, var);
        for(point p:b.points){
            if(var.equals(getName(0))){
                high = p.temp > high? p.temp : high;
            }
            else if(var.equals(getName(1))){
                high = p.grav > high? p.grav : high;
            }
            else{
                high = p.co2 > high? p.co2 : high;
            }
        }

        g.getViewport().setMaxY(high);

        //g.setTitle(var);
        g.addSeries(data);
        Log.d("Points", "Done");
    }

    void beginListenForData()
    {
        final Handler handler = new Handler();

        stopWorker = false;
        workerThread = new Thread(new Runnable()
        {
            public void run()
            {

                while(!Thread.currentThread().isInterrupted() && !stopWorker)
                {
                    final GraphView g[] = {(GraphView) findViewById(R.id.graph1),(GraphView) findViewById(R.id.graph2),(GraphView) findViewById(R.id.graph3)};
                    try
                    {
                        if(mmInputStream.available() > 0)
                        {
                            final String recvdata = parseBytes(mmInputStream);
                            Log.d("Basic","loop");

                            if(recvdata.equals("S_ACK")){
                                handler.post(new Runnable()
                                {
                                    public void run()
                                    {
                                        try{
                                            sendData("dataReq");
                                        }
                                        catch (IOException ex){
                                        }
                                    }
                                });
                                Log.d("Listener","Start acknowledged");
                                continue;
                            }
                            else if(recvdata.equals("data_begin")){
                                dataBegin = 1;
                                Log.d("Listener","Data begin");
                                /*handler.post(new Runnable()
                                {
                                    public void run()
                                    {
                                        Toast.makeText(getApplication().getBaseContext(), "DATA BEGIN", Toast.LENGTH_LONG).show();
                                    }
                                });*/
                            }
                            else if(recvdata.equals("data_end")){
                                dataBegin = 0;
                                Log.d("Listener","data end");
                                if(state == 2){
                                    Log.d("Listener","Changed state from brewing to normal");
                                    state = 0;
                                }
                                handler.post(new Runnable()
                                {
                                    public void run()
                                    {

                                        if(state == 2){
                                            for(int i = 0; i < 3; i++) {
                                                g[i].removeAllSeries();
                                                graph(g[i], results, getName(i));
                                            }
                                        }

                                        findViewById(R.id.button2).performClick();

                                    }
                                });
                            }
                            else if(dataBegin.compareTo(1) == 0) {
                                Log.d("Listener","Point received");
                                handler.post(new Runnable()
                                {
                                    public void run()
                                    {
                                        results.points.add(point.parseJSON(recvdata));
                                        if(state == 2){
                                            for(int i = 0; i < 3; i++) {
                                                g[i].removeAllSeries();
                                                graph(g[i], results, getName(i));
                                            }
                                        }

                                    }});
                            }
                            handler.post(new Runnable()
                            {
                                public void run()
                                {
                                    try{
                                        sendData("ACK");
                                    }
                                    catch (IOException ex){
                                    }
                                }
                                });
                        }
                    }
                    catch (IOException ex)
                    {
                        stopWorker = true;
                    }
                }
            }
        });

        workerThread.start();
    }

    void sendData(String str) throws IOException
    {
        if (mmOutputStream != null && str != null) {
            str += "\n";
            mmOutputStream.write(str.getBytes());
            //myLabel.setText("Data Sent");
        }
    }

    void closeBT() throws IOException
    {
        if(mmOutputStream != null && mmInputStream != null) {
            stopWorker = true;
            mmOutputStream.close();
            mmInputStream.close();
            mmSocket.close();
            //myLabel.setText("Bluetooth Closed");
        }
    }
}