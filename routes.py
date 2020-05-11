from flask import Flask, render_template, flash,redirect
from forms import EncryptForm, DecryptForm

from EnigmaMachine import EnigmaMachine
enigma_machine = EnigmaMachine()

app = Flask(__name__)

#Flask-WTF extension uses to protect web forms against Cross-Site Request Forgery
app.config['SECRET_KEY'] = 'you-will-never-guess'

rotor_positions = (0,0,0)

@app.route("/" ,    methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
	encrypt_form = EncryptForm()
	decrypt_form = DecryptForm()
	global rotor_positions

	if encrypt_form.validate_on_submit():
		plain_text  = encrypt_form.plaintext.data
		rotor_positions, cypher_text = enigma_machine.encode(plain_text)

		flash(cypher_text, category='success')

		return render_template('home.html', title='EnigPy',
		encrypt_form=encrypt_form, decrypt_form=decrypt_form, cypher_text=cypher_text, encrypt=True)

	if decrypt_form.validate_on_submit():
		cypher_text     = decrypt_form.cyphertext.data
		plain_text      = enigma_machine.encode(cypher_text, rotor_positions, decrypt=True)

		flash(plain_text, category='success')

		return render_template('home.html', title='EnigPy',
			encrypt_form=encrypt_form, decrypt_form=decrypt_form, plain_text=plain_text, encrypt=False)

	return render_template('home.html', title='EnigPy',
		encrypt_form=encrypt_form, decrypt_form=decrypt_form, encrypt=False)


if __name__ == '__main__':
    app.run(debug=True)