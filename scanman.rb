class Scanman < Formula
  include Language::Python::Virtualenv

  desc "Using LLMs to interact with man pages"
  url "https://github.com/nikhilkmr300/scanman/archive/refs/tags/1.0.0.tar.gz"
  sha256 "0682e815dc203514a42a8eb0d8808ba00b4ed636849afe2f2295ea4154f7f0e8"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
    bin.install "src/scanman"
  end
end
