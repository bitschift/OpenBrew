package brew.ai;



import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.graphics.Color;
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
    TextView myLabel;
    TextView Label;
    EditText myTextbox;
    BluetoothAdapter mBluetoothAdapter;
    BluetoothSocket mmSocket;
    BluetoothDevice mmDevice;
    OutputStream mmOutputStream;
    InputStream mmInputStream;
    Thread workerThread;
    byte[] readBuffer;
    int readBufferPosition;
    volatile boolean stopWorker;
    ArrayList<String> unrefined_points;
    batch results;
    String data = "";
    int state = 0; // 0 is normal, 1 is pre-brew, 2 is brewing, 3 is post brew
    Integer dataBegin = 0;
    GraphView graph;



    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button openButton = (Button)findViewById(R.id.open);
        Button sendButton = (Button)findViewById(R.id.send);
        Button closeButton = (Button)findViewById(R.id.close);
        myLabel = (TextView)findViewById(R.id.label);
        myTextbox = (EditText)findViewById(R.id.entry);
        Label = (TextView)findViewById(R.id.recv);;
        graph = (GraphView) findViewById(R.id.graph1);
        unrefined_points = new ArrayList<String>();
        results = new batch();

        //Send Button
        sendButton.setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View v)
            {
                try
                {
                    String msg = myTextbox.getText().toString();
                    sendData(msg);
                }
                catch (IOException ex) { }
            }
        });

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

        try {
            sendData("start");
        }
        catch(IOException e){}
    }

    void findBT()
    {
        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if(mBluetoothAdapter == null)
        {
            myLabel.setText("No bluetooth adapter available");
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
                    myLabel.setText("Bluetooth Device Found");
                    break;
                //}
            }
        }
    }

    void openBT() throws IOException {
        if (mmDevice != null) {
            UUID uuid = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee"); //Standard SerialPortService ID
            mmSocket = mmDevice.createInsecureRfcommSocketToServiceRecord(uuid);
            mmSocket.connect();
            mmOutputStream = mmSocket.getOutputStream();
            mmInputStream = mmSocket.getInputStream();

            beginListenForData();

            myLabel.setText("Bluetooth Opened");
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

    String getName(String str){
        if(str.equals("grav")){
            return getResources().getString(R.string.grav);
        }
        else if(str.equals("co2")){
            return getResources().getString(R.string.co2);
        }
        else if(str.equals("temp")){
            return getResources().getString(R.string.temp);
        }
        return "";
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

        g.getViewport().setMinX(0);
        g.getViewport().setMaxX(b.points.get(b.points.size()-1).time);
        g.getViewport().setMinY(0);
        g.getViewport().setMaxY(60);
        g.getViewport().setYAxisBoundsManual(true);
        g.getViewport().setXAxisBoundsManual(true);

        LineGraphSeries<DataPoint> data = getDataPoints(b, var);

        data.setTitle(var);
        /*g.getLegendRenderer().setVisible(true);
        g.getLegendRenderer().setAlign(LegendRenderer.LegendAlign.TOP);
        g.getLegendRenderer().setBackgroundColor(Color.alpha(0));*/


        g.setTitle(var);
        g.addSeries(data);
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
                    try
                    {
                        if(mmInputStream.available() > 0)
                        {
                            final String recvdata = parseBytes(mmInputStream);

                            if(recvdata.equals("data_begin")){
                                dataBegin = 1;
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
                                handler.post(new Runnable()
                                {
                                    public void run()
                                    {
                                        //Label.setText("RealData");
                                        //for(String s: unrefined_points){
                                        //    Label.append(s);
                                        //}
                                        graph((GraphView) findViewById(R.id.graph1), results, getName("grav"));
                                        //Toast.makeText(getApplication().getBaseContext(), "DATA END", Toast.LENGTH_LONG).show();
                                    }
                                });
                            }
                            else if(dataBegin.compareTo(1) == 0) {
                                handler.post(new Runnable()
                                {
                                    public void run()
                                    {
                                        results.points.add(point.parseJSON(recvdata));
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
            myLabel.setText("Data Sent");
        }
    }

    void closeBT() throws IOException
    {
        if(mmOutputStream != null && mmInputStream != null) {
            stopWorker = true;
            mmOutputStream.close();
            mmInputStream.close();
            mmSocket.close();
            myLabel.setText("Bluetooth Closed");
        }
    }
}