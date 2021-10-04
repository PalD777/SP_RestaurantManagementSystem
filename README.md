<!-- MIT License

Copyright (c) 2021 Othneil Drew

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. -->
<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/PalD777/SP_RestaurantManagementSystem">
    <img src="src/client/static/images/logo.png" alt="Logo" width="150" height="60">
  </a>

<h3 align="center">S&P Restaurant Management System</h3>

  <p align="center">
    A client and server Restaurant ordering system
    <br />
    <a href="https://github.com/PalD777/SP_RestaurantManagementSystem"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/PalD777/SP_RestaurantManagementSystem/issues">Report Bug</a>
    ·
    <a href="https://github.com/PalD777/SP_RestaurantManagementSystem/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `PalD777`, `SP_RestaurantManagementSystem`, `twitter_handle`, `linkedin_username`, `email`, `email_client`, `project_title`, `project_description`

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Kivy](https://kivy.org)
* [MySQL](https://www.mysql.com/)
* [Owl Carousel](https://owlcarousel2.github.io/OwlCarousel2/)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Download and install the latest version of [MySQL](https://dev.mysql.com/downloads/installer/).
Create a schema `restaurant` and make sure the user that you are using to access it has `SELECT`, 
`INSERT`, `UPDATE`, `DROP`
* After setting up the schema, run these query in it.
  ```sql
  CREATE TABLE menu (id VARCHAR(255), item TEXT, descr MEDIUMTEXT, price DECIMAL(10,3), img LONGTEXT)
  CREATE TABLE orders (id INT, table_num INT, total DECIMAL(10,3), order_done TINYINT, items TEXT)
  ```
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/PalD777/SP_RestaurantManagementSystem.git
   ```
2. Install necessary libraries
   ```sh
   pip install -r requirements.txt
   ```
3. Find and replace `user` and `password` in every `mysql.connector.connect` call with your own in the files `server.py`, `app.py`, `sql_helper.py`
4. Run `sql_helper.py` with `menu` as an argument to update database
   ```sh
   python3 src/server/sql_helper.py menu
   ```


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

* To run restaurant server:
    ```
    python3 src/server/server.py [-h] [-u] [-p PORT]

    optional arguments:
      -h, --help            Shows the help message and exits
      -u, --ui, --show-ui   Specifies whether to show UI containing unserved orders and a remove button
      -p PORT, --port PORT  Specifies a custom Server port [default: 9999]
    ```
* To run the client:
    ```
    python3 src/client/client.py [-h] [-s IP] [-p SERVER_PORT] [-f FLASK_PORT]

    optional arguments:
      -h, --help            Shows the help message and exits
      -s IP, --sip IP, --server-ip IP
                            Specifies Server IP Address [default: 127.0.0.1]
      -p SERVER_PORT, --sp SERVER_PORT, --s-port SERVER_PORT, --server-port SERVER_PORT
                            Specifies Server port [default: 9999]
      -f FLASK_PORT, --fp FLASK_PORT, --f-port FLASK_PORT, --flask-ip FLASK_PORT
                            Specifies Flask App port [default: 5000]
    ```
* To use the sql_helper:
    ```
    python3 src/server/sql_helper.py
    positional arguments:
      modification_target   Specifies what to modify. Possible values: menu, orders, both
                            menu => updates the menu
                            orders => resets orders table [WARNING: All current order data will be lost]
                            both => does both

    optional arguments:
      -h, --help            shows the help message and exits
    ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [KlassyCafe - Templatemo](https://templatemo.com/tm-558-klassy-cafe)
* [Best README Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/PalD777/SP_RestaurantManagementSystem.svg?style=for-the-badge
[contributors-url]: https://github.com/PalD777/SP_RestaurantManagementSystem/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/PalD777/SP_RestaurantManagementSystem.svg?style=for-the-badge
[forks-url]: https://github.com/PalD777/SP_RestaurantManagementSystem/network/members
[stars-shield]: https://img.shields.io/github/stars/PalD777/SP_RestaurantManagementSystem.svg?style=for-the-badge
[stars-url]: https://github.com/PalD777/SP_RestaurantManagementSystem/stargazers
[issues-shield]: https://img.shields.io/github/issues/PalD777/SP_RestaurantManagementSystem.svg?style=for-the-badge
[issues-url]: https://github.com/PalD777/SP_RestaurantManagementSystem/issues
[license-shield]: https://img.shields.io/github/license/PalD777/SP_RestaurantManagementSystem.svg?style=for-the-badge
[license-url]: https://github.com/PalD777/SP_RestaurantManagementSystem/blob/master/LICENSE.txt
[product-screenshot]: src/client/static/images/screenshot.png
