#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <iomanip>

struct Bar {
    std::string date;
    double close;
};

class Backtest {
public:
    Backtest(const std::string& fileName) {
        loadCSV(fileName);
    }

    void run() {
        double shortTermMA = 0;
        double longTermMA = 0;
        double shortTermSum = 0;
        double longTermSum = 0;
        int shortTermWindow = 50;
        int longTermWindow = 200;
        int shortTermCount = 0;
        int longTermCount = 0;

        double initialBalance = 10000.0;
        double balance = initialBalance;
        bool isPositionOpen = false;
        int positionSize = 0;

        for (size_t i = 0; i < data.size(); ++i) {
            const Bar& bar = data[i];
            
            shortTermSum += bar.close;
            longTermSum += bar.close;

            if (shortTermCount < shortTermWindow) {
                shortTermCount++;
            } else {
                shortTermSum -= data[i - shortTermWindow].close;
            }

            if (longTermCount < longTermWindow) {
                longTermCount++;
            } else {
                longTermSum -= data[i - longTermWindow].close;
            }

            if (shortTermCount == shortTermWindow) {
                shortTermMA = shortTermSum / shortTermWindow;
            }

            if (longTermCount == longTermWindow) {
                longTermMA = longTermSum / longTermWindow;
            }

            if (i >= longTermWindow) {
                if (shortTermMA > longTermMA && !isPositionOpen) {
                    positionSize = balance / bar.close;
                    balance -= positionSize * bar.close;
                    isPositionOpen = true;
                    std::cout << "Buying at: " << bar.date << " Price: " << bar.close << " Balance: " << balance << "\n";
                } else if (shortTermMA < longTermMA && isPositionOpen) {
                    balance += positionSize * bar.close;
                    positionSize = 0;
                    isPositionOpen = false;
                    std::cout << "Selling at: " << bar.date << " Price: " << bar.close << " Balance: " << balance << "\n";
                }
            }
        }

        if (isPositionOpen) {
            balance += positionSize * data.back().close;
            std::cout << "Closing position at: " << data.back().date << " Price: " << data.back().close << " Final Balance: " << balance << "\n";
        }

        std::cout << "Initial balance: " << initialBalance << "\n";
        std::cout << "Final balance: " << balance << "\n";
    }

private:
    std::vector<Bar> data;

    void loadCSV(const std::string& fileName) {
        std::ifstream file(fileName);
        std::string line;
        
        while (std::getline(file, line)) {
            std::stringstream ss(line);
            Bar bar;
            std::string temp;
            
            std::getline(ss, bar.date, ',');
            std::getline(ss, temp, ',');
            
            try {
                bar.close = std::stod(temp);
            } catch (const std::invalid_argument& e) {
                std::cerr << "Invalid value for close price in line: " << line << "\n";
                continue;
            }
            
            data.push_back(bar);
        }
    }
};

int main() {
    Backtest backtest("temp_data.csv");
    backtest.run();
    return 0;
}
