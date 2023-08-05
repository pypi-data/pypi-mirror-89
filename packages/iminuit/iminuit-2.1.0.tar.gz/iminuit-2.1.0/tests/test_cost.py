import pytest
import numpy as np
from numpy.testing import assert_allclose
from iminuit import Minuit
from iminuit.cost import (
    UnbinnedNLL,
    BinnedNLL,
    ExtendedUnbinnedNLL,
    ExtendedBinnedNLL,
    LeastSquares,
)

stats = pytest.importorskip("scipy.stats")
norm = stats.norm


def expon_cdf(x, a):
    return 1 - np.exp(-x / a)


@pytest.fixture
def unbinned():
    np.random.seed(1)
    x = np.random.randn(1000)
    mle = (len(x), np.mean(x), np.std(x, ddof=1))
    return mle, x


@pytest.fixture
def binned(unbinned):
    mle, x = unbinned
    nx, xe = np.histogram(x, bins=50, range=(-3, 3))
    return mle, nx, xe


@pytest.mark.parametrize("verbose", (0, 1))
def test_UnbinnedNLL(unbinned, verbose):
    mle, x = unbinned

    def pdf(x, mu, sigma):
        return norm(mu, sigma).pdf(x)

    cost = UnbinnedNLL(x, pdf, verbose=verbose)
    m = Minuit(cost, mu=0, sigma=1)
    m.limits["sigma"] = (0, None)
    m.migrad()
    assert_allclose(m.values, mle[1:], atol=1e-3)
    assert m.errors["mu"] == pytest.approx(1000 ** -0.5, rel=0.05)


@pytest.mark.parametrize("verbose", (0, 1))
def test_ExtendedUnbinnedNLL(unbinned, verbose):
    mle, x = unbinned

    def scaled_pdf(x, n, mu, sigma):
        return n, n * norm(mu, sigma).pdf(x)

    cost = ExtendedUnbinnedNLL(x, scaled_pdf, verbose=verbose)
    m = Minuit(cost, n=len(x), mu=0, sigma=1)
    m.limits["n"] = (0, None)
    m.limits["sigma"] = (0, None)
    m.migrad()
    assert_allclose(m.values, mle, atol=1e-3)
    assert m.errors["mu"] == pytest.approx(1000 ** -0.5, rel=0.05)


@pytest.mark.parametrize("verbose", (0, 1))
def test_BinnedNLL(binned, verbose):
    mle, nx, xe = binned

    def cdf(x, mu, sigma):
        return norm(mu, sigma).cdf(x)

    cost = BinnedNLL(nx, xe, cdf, verbose=verbose)
    m = Minuit(cost, mu=0, sigma=1)
    m.limits["sigma"] = (0, None)
    m.migrad()
    # binning loses information compared to unbinned case
    assert_allclose(m.values, mle[1:], rtol=0.15)
    assert m.errors["mu"] == pytest.approx(1000 ** -0.5, rel=0.05)


def test_BinnedNLL_bad_input():
    with pytest.raises(ValueError):
        BinnedNLL([1], [1], lambda x, a: 0)


@pytest.mark.parametrize("verbose", (0, 1))
def test_ExtendedBinnedNLL(binned, verbose):
    mle, nx, xe = binned

    def scaled_cdf(x, n, mu, sigma):
        return n * norm(mu, sigma).cdf(x)

    cost = ExtendedBinnedNLL(nx, xe, scaled_cdf, verbose=verbose)
    m = Minuit(cost, n=mle[0], mu=0, sigma=1)
    m.limits["n"] = (0, None)
    m.limits["sigma"] = (0, None)
    m.migrad()
    # binning loses information compared to unbinned case
    assert_allclose(m.values, mle, rtol=0.15)
    assert m.errors["mu"] == pytest.approx(1000 ** -0.5, rel=0.05)


def test_ExtendedBinnedNLL_bad_input():
    with pytest.raises(ValueError):
        ExtendedBinnedNLL([1], [1], lambda x, a: 0)


@pytest.mark.parametrize("loss", ["linear", "soft_l1", np.arctan])
@pytest.mark.parametrize("verbose", (0, 1))
def test_LeastSquares(loss, verbose):
    np.random.seed(1)
    x = np.random.rand(20)
    y = 2 * x + 1
    ye = 0.1
    y += ye * np.random.randn(len(y))

    def model(x, a, b):
        return a + b * x

    cost = LeastSquares(x, y, ye, model, loss=loss, verbose=verbose)
    m = Minuit(cost, a=0, b=0)
    m.migrad()
    assert_allclose(m.values, (1, 2), rtol=0.03)
    assert cost.loss == loss
    if loss != "linear":
        cost.loss = "linear"
        assert cost.loss != loss
    m.migrad()
    assert_allclose(m.values, (1, 2), rtol=0.02)


def test_LeastSquares_bad_input():
    with pytest.raises(ValueError):
        LeastSquares([1, 2], [1], [1], lambda x, a: 0)

    with pytest.raises(ValueError):
        LeastSquares([1, 2], [1, 2], [1], lambda x, a: 0)

    with pytest.raises(ValueError):
        LeastSquares([1], [1], [1], lambda x, a: 0, loss="foo")


def test_UnbinnedNLL_mask():
    c = UnbinnedNLL([1, np.nan, 2], lambda x, a: x + a)

    assert np.isnan(c(0)) == True
    c.mask = np.arange(3) != 1
    assert np.isnan(c(0)) == False


def test_ExtendedUnbinnedNLL_mask():
    c = ExtendedUnbinnedNLL([1, np.nan, 2], lambda x, a: (1, x + a))

    assert np.isnan(c(0)) == True
    c.mask = np.arange(3) != 1
    assert np.isnan(c(0)) == False


def test_BinnedNLL_mask():

    c = BinnedNLL([5, 1000, 1], [0, 1, 2, 3], expon_cdf)

    c_unmasked = c(1)
    c.mask = np.arange(3) != 1
    assert c(1) < c_unmasked


def test_ExtendedBinnedNLL_mask():
    c = ExtendedBinnedNLL([1, 1000, 2], [0, 1, 2, 3], expon_cdf)

    c_unmasked = c(2)
    c.mask = np.arange(3) != 1
    assert c(2) < c_unmasked


def test_LeastSquares_mask():
    c = LeastSquares([1, 2, 3], [3, np.nan, 4], [1, 1, 1], lambda x, a: x + a)
    assert np.isnan(c(0)) == True
    c.mask = np.arange(3) != 1
    assert np.isnan(c(0)) == False
