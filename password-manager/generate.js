const upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const lower = "abcdefghijklmnopqrstuvwxyz"
const numbers = "1234567890";
const special = "~!@#$%^&*_+=|<>?";

const randUpper = () => {
    let index = Math.floor(Math.random() * 26);
    return upper[index];
}

const randLower = () => {
    let index = Math.floor(Math.random() * 26);
    return lower[index];
}

const randNumber = () => {
    let index = Math.floor(Math.random() * 10);
    return numbers[index];
}

const randSpecial = () => {
    let index = Math.floor(Math.random() * 16);
    return special[index];
}

let password = ""

for (let i = 0; i < 4; i++) {
    let order = Math.floor(Math.random() * 4)
    switch (order) {
        case 0:
            password += randLower();
            password += randSpecial();
            password += randUpper();
            password += randNumber();
        case 1:
            password += randSpecial();
            password += randUpper();
            password += randNumber();
            password += randLower();
        case 2:
            password += randUpper();
            password += randNumber();
            password += randLower();
            password += randSpecial();
        case 3:
            password += randNumber();
            password += randLower();
            password += randSpecial();
            password += randUpper();
    }
}

console.log(password);