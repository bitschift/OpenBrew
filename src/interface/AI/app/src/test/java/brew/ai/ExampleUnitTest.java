package brew.ai;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Example local unit test, which will execute on the development machine (host).
 *
 * @see <a href="http://d.android.com/tools/testing">Testing documentation</a>
 */
public class ExampleUnitTest {
    @Test
    public void addition_isCorrect() throws Exception {
        assertEquals(4, 2 + 2);
    }
    @Test
    public void JSONtranslation() throws Exception {
        String str = "{\'temp\':12.0,\'co2\':1.0,\'grav\':13.1,\'time\':12}";
        point p = point.parseJSON(str);
        assertNotNull(p);
        assertEquals(p.temp, 12.0, 0);
    }
}