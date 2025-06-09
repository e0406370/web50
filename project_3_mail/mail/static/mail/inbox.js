document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));

  // Task 1: Send email via compose form
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';  
  document.querySelector('#compose-body').value = '';
}

/**
 * @param {string} mailbox
 */
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`, {
    method: "GET"
  })
    .then(resp => resp.json())
    .then(data => {
      if (data.length === 0) {
        const emptyMailbox = document.createElement('div');
        emptyMailbox.classList.add('alert', 'alert-info','text-center', 'font-weight-bold');
        emptyMailbox.innerHTML = 'This mailbox is empty. You are all caught up!';

        document.querySelector("#emails-view").append(emptyMailbox);
      }
      else {
        const emailContainer = document.createElement('div');
        emailContainer.classList.add('container');

        data.forEach(email => {
          const emailRow = document.createElement('div');
          emailRow.classList.add('row', 'border', 'border-dark', 'mb-2', (email.read ? 'bg-white' : 'bg-secondary'));
          emailContainer.appendChild(emailRow);

          const emailColSender = document.createElement('div');
          emailColSender.classList.add('col', 'text-left', 'font-weight-bold');
          emailColSender.innerHTML = email.sender;
          emailRow.appendChild(emailColSender);

          const emailColSubject = document.createElement('div');
          emailColSubject.classList.add('col', 'font-weight-bold');
          emailColSubject.innerHTML = email.subject;
          emailRow.appendChild(emailColSubject);

          const emailColTimestamp = document.createElement('div');
          emailColTimestamp.classList.add('col', 'text-right', 'font-weight-bold');
          emailColTimestamp.innerHTML = email.timestamp;
          emailRow.appendChild(emailColTimestamp);
        });

        document.querySelector("#emails-view").append(emailContainer);
      }
    })
}


/**
 * @param {SubmitEvent} event
 */
function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then(resp => resp.json().then(data => {
      if (!resp.ok) {
        alert(data.error);
      }
      else {
        alert(data.message);
        load_mailbox('sent');
      }
    }))
}