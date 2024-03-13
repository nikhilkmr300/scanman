class Scanman < Formula
  include Language::Python::Virtualenv

  desc "Using LLMs to interact with man pages"
  url "https://github.com/nikhilkmr300/scanman/archive/refs/tags/1.0.3.tar.gz"
  sha256 "9e90b570b5e494558dd695b5a9db389a9bb7666f76fba39f04f2b85c3a3412fc"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
    bin.install "src/scanman"
  end
end
