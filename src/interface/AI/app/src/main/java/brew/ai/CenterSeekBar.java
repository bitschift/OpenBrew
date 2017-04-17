package brew.ai;

/**
 * Created by cody on 4/16/17.
 * Code from http://stackoverflow.com/questions/17415096/seekbar-for-two-values-50-0-50
 */
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.widget.SeekBar;

public class CenterSeekBar extends android.support.v7.widget.AppCompatSeekBar {

    private Rect rect;
    private Paint paint ;
    private int seekbar_height;

    public CenterSeekBar(Context context) {
        super(context);
    }

    public CenterSeekBar(Context context, AttributeSet attrs) {
        super(context, attrs);
        rect = new Rect();
        paint = new Paint();
        seekbar_height = 6;
    }

    public CenterSeekBar(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
    }

    @Override
    protected synchronized void onDraw(Canvas canvas) {

        rect.set(getThumbOffset(),
                (getHeight() / 2) - (seekbar_height/2),
                getWidth()- getThumbOffset(),
                (getHeight() / 2) + (seekbar_height/2));

        paint.setColor(Color.GRAY);

        canvas.drawRect(rect, paint);



        if (this.getProgress() > 50) {


            rect.set(getWidth() / 2,
                    (getHeight() / 2) - (seekbar_height/2),
                    getWidth() / 2 + (getWidth() / 100) * (getProgress() - 50),
                    getHeight() / 2 + (seekbar_height/2));

            paint.setColor(Color.CYAN);
            canvas.drawRect(rect, paint);

        }

        if (this.getProgress() < 50) {

            rect.set(getWidth() / 2 - ((getWidth() / 100) * (50 - getProgress())),
                    (getHeight() / 2) - (seekbar_height/2),
                    getWidth() / 2,
                    getHeight() / 2 + (seekbar_height/2));

            paint.setColor(Color.CYAN);
            canvas.drawRect(rect, paint);

        }

        super.onDraw(canvas);
    }
}