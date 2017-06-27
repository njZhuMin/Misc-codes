package json;

import bean.Person;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class JSONObjectSample {

    public static void main(String[] args) {
//        jSONObjectSample();
//        createJSONByMap();
        createJSONByBean();
    }

    private static void jSONObjectSample() {
        JSONObject laowang = new JSONObject();
        try {
            laowang.put("name", "隔壁老王");
            laowang.put("age", 25);
            laowang.put("birthday", "1990-01-01");
            laowang.put("school", "蓝翔");
            laowang.put("major", new String[] {"挖掘机", "计算机"});
            laowang.put("has_girlfriend", false);
            laowang.put("car", JSONObject.NULL);
            laowang.put("house", JSONObject.NULL);
            laowang.put("comment", "这是一个注释");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        System.out.println(laowang.toString());
    }

    private static void createJSONByMap() {
        Map<String, Object> laowang = new HashMap<String, Object>();
        laowang.put("name", "隔壁老王");
        laowang.put("age", 25);
        laowang.put("birthday", "1990-01-01");
        laowang.put("school", "蓝翔");
        laowang.put("major", new String[] {"挖掘机", "计算机"});
        laowang.put("has_girlfriend", false);
        laowang.put("car", JSONObject.NULL);
        laowang.put("house", JSONObject.NULL);
        laowang.put("comment", "这是一个注释");
        System.out.println(new JSONObject(laowang).toString());
    }

    private static void createJSONByBean() {
        Person laowang = new Person();
        laowang.setName("隔壁老王");
        laowang.setAge(25);
        laowang.setBirthday("1990-01-01");
        laowang.setSchool("蓝翔");
        laowang.setMajor(new String[] {"挖掘机", "计算机"});
        laowang.setHas_girlfriend(false);
        laowang.setCar(JSONObject.NULL);
        laowang.setHouse(JSONObject.NULL);
        laowang.setComment("这是一个注释");
        System.out.println(new JSONObject(laowang));
    }
}
