import java.sql.Connection;
import java.sql.Statement;

// CodeQL은 사용자 입력(source)이 안전한 처리(sanitizer) 없이
// 위험한 함수(sink)로 흘러 들어가는지 (Data Flow)를 분석합니다.

public class UserService {

    // CodeQL Source: @RequestParam username (사용자 입력)
    public void getUserData(String username) {
        
        try (Connection conn = getConnection()) {
            
            // ❌ CodeQL 탐지 지점: SQL Injection
            // 사용자 입력(username)이 문자열 연결을 통해 바로 SQL 쿼리에 삽입됩니다.
            // CodeQL Sink: statement.executeQuery()
            String query = "SELECT * FROM users WHERE username = '" + username + "'"; 
            
            Statement statement = conn.createStatement();
            statement.executeQuery(query); // 👈 CodeQL이 'sink'로 판단

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    private Connection getConnection() {
        // ... DB 연결 로직 (생략)
        return null;
    }
}
//